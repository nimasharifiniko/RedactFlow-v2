import fitz
from docx import Document
from docx.shared import Inches
import os
import tempfile
import cv2
from PIL import Image


def export_to_pdf(image, output_path: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp_path = tmp.name
        cv2.imwrite(tmp_path, image)

    try:
        doc = fitz.open()
        img_pdf = fitz.open(tmp_path)
        pdfbytes = img_pdf.convert_to_pdf()
        img_pdf.close()

        pdf_doc = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(pdf_doc)
        doc.save(output_path)
        doc.close()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def export_to_docx(image, output_path: str):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_image)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp_path = tmp.name
        pil_img.save(tmp_path)

    try:
        doc = Document()
        doc.add_picture(tmp_path, width=Inches(6.0))
        doc.save(output_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
