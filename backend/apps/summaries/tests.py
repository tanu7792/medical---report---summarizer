
from django.test import TestCase
from apps.reports.utils import extract_text_from_pdf

class PDFUtilsTest(TestCase):
    def test_pdf_extraction(self):
        text = extract_text_from_pdf("sample.pdf")
        self.assertTrue(len(text) > 0)


# Create your tests here.
