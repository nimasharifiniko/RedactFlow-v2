import pymupdf
from docx import Document
import os
from datetime import datetime

def clean_pdf_metadata(input_path: str, output_path: str):
    doc = pymupdf.open(input_path)
    
    doc.set_metadata({
        "author": "",
        "producer": "RedactFlow",
        "creator": "RedactFlow",
        "title": "",
        "subject": "",
        "keywords": ""
    })
    
    doc.del_xml_metadata()
    doc.save(output_path, garbage=3, deflate=True)
    doc.close()


def clean_docx_metadata(input_path: str, output_path: str):
    doc = Document(input_path)
    
    core = doc.core_properties
    core.author = ""
    core.category = ""
    core.comments = ""
    core.content_status = ""
    
    # docx library requires datetime objects, not None
    safe_date = datetime(2000, 1, 1, 0, 0, 0)
    core.created = safe_date
    core.modified = safe_date
    core.last_printed = safe_date
    
    core.identifier = ""
    core.keywords = ""
    core.language = ""
    core.last_modified_by = ""
    core.revision = 1
    core.subject = ""
    core.title = ""
    core.version = ""
    
    doc.save(output_path)


def scrub_metadata(input_path: str, output_path: str):
    ext = os.path.splitext(input_path)[1].lower()
    
    if ext == ".pdf":
        clean_pdf_metadata(input_path, output_path)
    elif ext == ".docx":
        clean_docx_metadata(input_path, output_path)
    else:
        raise ValueError(f"Unsupported file type for metadata scrubbing: {ext}")