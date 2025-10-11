from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import MedicalReport
from .serializers import ReportSerializer
from .utils import extract_text_from_pdf, extract_text_from_docx

class ReportViewSet(viewsets.ModelViewSet):
    queryset = MedicalReport.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return MedicalReport.objects.filter(user=self.request.user).order_by("-uploaded_at")

    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user)
        f = report.original_file
        text = ""
        if f:
            fpath = f.path
            name = f.name.lower()
            if name.endswith(".pdf"):
                text = extract_text_from_pdf(fpath)
            elif name.endswith(".docx"):
                text = extract_text_from_docx(fpath)
            else:
                try:
                    text = open(fpath, "r", encoding="utf-8", errors="ignore").read()
                except Exception:
                    text = ""
        report.extracted_text = text
        report.save()
