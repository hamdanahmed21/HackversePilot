"""
policy_parser.py
AI Meeting Watchdog — Policy document text extraction

Takes raw uploaded file bytes + filename, returns plain text.
Supports: .pdf, .txt, .docx

This module does ONLY extraction. Splitting the text into discrete
rule clauses is handled by rule_extractor.py (uses the LLM).
"""

import io

from pypdf import PdfReader
from docx import Document


class UnsupportedFileType(Exception):
    pass


def extract_text(filename: str, file_bytes: bytes) -> str:
    """
    Dispatches to the right extractor based on file extension.

    Args:
        filename: original filename, e.g. "policy.pdf"
        file_bytes: raw bytes of the uploaded file

    Returns:
        Plain text content of the document.

    Raises:
        UnsupportedFileType: if the extension isn't .pdf, .txt, or .docx
    """
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if ext == "pdf":
        return _extract_pdf(file_bytes)
    elif ext == "txt":
        return _extract_txt(file_bytes)
    elif ext == "docx":
        return _extract_docx(file_bytes)
    else:
        raise UnsupportedFileType(
            f"Unsupported file type: '.{ext}'. Please upload a .pdf, .txt, or .docx file."
        )


def _extract_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def _extract_txt(file_bytes: bytes) -> str:
    # Try utf-8 first, fall back to latin-1 so we never hard-crash on encoding
    try:
        return file_bytes.decode("utf-8").strip()
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1").strip()


def _extract_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()
