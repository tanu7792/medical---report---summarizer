# This file implements a synchronous summarizer for simplicity.
# Later you can replace with Celery tasks for background processing.
from apps.reports.models import Report
from .models import Summary
from django.conf import settings

# Prefer HF; fallback to simple summarizer repeat
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    _hf_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception:
    _hf_summarizer = None

# Optional OpenAI integration (if API key provided)
try:
    import openai
    openai.api_key = settings.OPENAI_API_KEY
    _openai_available = bool(settings.OPENAI_API_KEY)
except Exception:
    _openai_available = False

def chunk_text(text, max_chars=3000):
    # naive chunker: split on paragraphs close to max_chars
    paragraphs = [p for p in text.split("\n") if p.strip()]
    chunks = []
    cur = ""
    for p in paragraphs:
        if len(cur) + len(p) + 1 > max_chars:
            chunks.append(cur)
            cur = p
        else:
            cur += "\n" + p
    if cur:
        chunks.append(cur)
    return chunks

def summarize_with_hf(text):
    if not _hf_summarizer:
        return ""
    chunks = chunk_text(text, max_chars=2000)
    parts = []
    for c in chunks:
        res = _hf_summarizer(c, max_length=200, min_length=40, do_sample=False)
        parts.append(res[0]["summary_text"])
    return "\n".join(parts)

def summarize_with_openai(text):
    if not _openai_available:
        return ""
    # chunk if too long - very naive
    chunks = chunk_text(text, max_chars=4000)
    summaries = []
    for c in chunks:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a concise medical summarizer."},
                {"role":"user","content":f"Summarize this medical report text into a concise structured summary with key findings and recommendations:\n\n{c}"}
            ],
            max_tokens=400,
        )
        summaries.append(resp.choices[0].message.content.strip())
    return "\n".join(summaries)

def summarize_report(report_id):
    report = Report.objects.get(id=report_id)
    text = report.extracted_text or ""
    if not text:
        return "No extractable text found."

    # prefer HF locally, else openai
    summary_text = ""
    if _hf_summarizer:
        try:
            summary_text = summarize_with_hf(text)
            method = "HF-bart-large-cnn"
        except Exception as e:
            summary_text = ""
    if not summary_text and _openai_available:
        summary_text = summarize_with_openai(text)
        method = "OpenAI-gpt"
    if not summary_text:
        # fallback naive: return first 800 chars
        summary_text = text[:800] + ("..." if len(text) > 800 else "")
        method = "fallback-truncate"

    Summary.objects.create(report=report, author=None, method=method, summary_text=summary_text, model_info={"method":method})
    return summary_text
