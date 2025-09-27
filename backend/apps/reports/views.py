from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from .utils.parser import extract_text_from_pdf, extract_text_from_docx

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Report.objects.filter(owner=self.request.user).order_by("-uploaded_at")

    def perform_create(self, serializer):
        report = serializer.save(owner=self.request.user, status="processing")
        # extract text synchronously for simplicity
        file_obj = report.original_file.open("rb")
        filename = report.original_file.name.lower()
        text = ""
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_obj)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file_obj)
        else:
            try:
                text = file_obj.read().decode(errors="ignore")
            except Exception:
                text = ""
        report.extracted_text = text
        report.status = "ready"
        report.save()

    @action(detail=True, methods=["post"])
    def summarize(self, request, pk=None):
        # call summarizer (synchronous stub)
        from apps.summaries.tasks import summarize_report
        report = self.get_object()
        summary_text = summarize_report(report.id)  # synchronous call here
        return Response({"summary": summary_text})
