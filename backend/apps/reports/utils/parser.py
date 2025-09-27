# Simple parsers: PDF (PyPDF2) and DOCX (python-docx). For scanned PDFs use pytesseract (OCR) - stubbed.
from PyPDF2 import PdfReader
import docx
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(file_obj):
    try:
        reader = PdfReader(file_obj)
        text = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text.append(t)
        full = "\n".join(text)
        if full.strip():
            return full
    except Exception:
        pass
    # fallback: OCR each page (requires converting pdf pages to images — not implemented here)
    return ""

def extract_text_from_docx(file_obj):
    try:
        doc = docx.Document(file_obj)
        paragraphs = [p.text for p in doc.paragraphs]
        return "\n".join(paragraphs)
    except Exception:
        return ""
