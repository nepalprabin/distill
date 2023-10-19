import requests
from io import BytesIO
import PyPDF2
from docx import Document

from fastapi import HTTPException


def parse_file(file_type, response):
    parsers = {
        "pdf": parse_pdf,
        "docx": parse_docx,
        "txt": parse_txt,
    }
    if file_type not in parsers:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Supported file types are PDF, DOCX, and TXT",
        )
    return parsers[file_type](response)


def parse_pdf(response):
    pdf_file = BytesIO(response.content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join(
        [pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))]
    )


def parse_docx(response):
    docx_file = BytesIO(response.content)
    doc = Document(docx_file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def parse_txt(response):
    return response.text
