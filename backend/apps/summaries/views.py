from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ReportSummary
from .serializers import SummarySerializer
from apps.reports.models import MedicalReport
from django.conf import settings
import openai, os, json

# local model imports (joblib)
import joblib
MODEL_PATH = os.path.join(settings.BASE_DIR, "diseases_model", "model.pkl")
VECT_PATH = os.path.join(settings.BASE_DIR, "diseases_model", "vectorizer.pkl")
_local_model = None
_vectorizer = None
if os.path.exists(MODEL_PATH) and os.path.exists(VECT_PATH):
    _local_model = joblib.load(MODEL_PATH)
    _vectorizer = joblib.load(VECT_PATH)

openai.api_key = settings.OPENAI_API_KEY

def llm_summarize(text):
    if not settings.OPENAI_API_KEY:
        return text[:800] + ("..." if len(text)>800 else "")
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are a concise medical summarizer."},
                  {"role":"user","content":f"Summarize the following medical report concisely for a clinician:\n\n{text}"}],
        max_tokens=400,
        temperature=0.0
    )
    return res.choices[0].message["content"].strip()

def llm_analyze_symptoms(text):
    if not settings.OPENAI_API_KEY:
        return "No OpenAI key"
    prompt = f"From the clinical text below, extract a list of symptoms (comma separated) and list possible diseases (short list). Text:\n\n{text}\n\nReturn JSON: {{'symptoms': [...], 'possible_diseases': [...]}}"
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=400,
        temperature=0.0
    )
    content = res.choices[0].message["content"].strip()
    # attempt to parse JSON from model response
    try:
        # model might return codeblock; extract first {...}
        import re
        m = re.search(r"\{.*\}", content, re.S)
        js = m.group(0) if m else content
        parsed = json.loads(js)
        return parsed
    except Exception:
        return {"raw": content}

def local_predict(symptom_text):
    if _local_model is None:
        return []
    X = _vectorizer.transform([symptom_text])
    preds = _local_model.predict_proba(X)
    classes = _local_model.classes_
    top_idxs = preds[0].argsort()[::-1][:5]
    return [{"disease": classes[i], "score": float(preds[0][i])} for i in top_idxs]

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = ReportSummary.objects.all()
    serializer_class = SummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReportSummary.objects.filter(report__user=self.request.user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        report_id = request.data.get("report")
        if not report_id:
            return Response({"detail":"report id required"}, status=status.HTTP_400_BAD_REQUEST)
        report = MedicalReport.objects.get(id=report_id, user=request.user)
        text = report.extracted_text or ""
        summary_text = llm_summarize(text)
        analysis = llm_analyze_symptoms(text)
        # predicted diseases from local model
        pred = []
        if isinstance(analysis, dict):
            symptom_text = ", ".join(analysis.get("symptoms", [])) if analysis.get("symptoms") else text[:500]
        else:
            symptom_text = text[:500]
        if _local_model:
            pred = local_predict(symptom_text)

        summ = ReportSummary.objects.create(report=report, summary_text=summary_text, analysis_text=json.dumps(analysis), predicted_diseases=json.dumps(pred))
        ser = self.get_serializer(summ)
        out = ser.data
        out["analysis_parsed"] = analysis
        out["predicted_diseases_parsed"] = pred
        return Response(out, status=status.HTTP_201_CREATED)
