from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(fpath_or_fileobj):
    try:
        reader = PdfReader(fpath_or_fileobj)
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    except Exception:
        return ""

def extract_text_from_docx(fpath_or_fileobj):
    try:
        doc = docx.Document(fpath_or_fileobj)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""
