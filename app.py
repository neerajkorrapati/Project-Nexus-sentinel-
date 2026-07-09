import io
import os
import uuid

import pdfplumber
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile

# Load API keys before engines read environment variables.
load_dotenv()

from pipeline.invoice_pipeline import InvoicePipeline
from engine.document_engine import DocumentEngine


app = FastAPI(title="Project Nexus Sentinel - Enterprise Invoice API")
pipeline = InvoicePipeline()
document_engine = DocumentEngine()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Reads PDF bytes with layout preservation to reduce column-boundary collapse
    during invoice parsing.
    """
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text(layout=True)
                if not extracted or not extracted.strip():
                    extracted = page.extract_text(layout=False) or ""
                text += extracted + "\n"
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read uploaded PDF: {exc}") from exc

    return text


def extract_text_with_ocr_fallback(file_bytes: bytes, filename: str) -> str:
    """
    First tries embedded PDF text. If the PDF is scanned/image-only, falls back
    to the OCR document engine.
    """
    embedded_text = extract_text_from_pdf(file_bytes)
    if embedded_text.strip():
        return embedded_text

    os.makedirs("uploads", exist_ok=True)
    safe_name = os.path.basename(filename or "invoice.pdf")
    temp_path = os.path.join("uploads", f"{uuid.uuid4().hex}_{safe_name}")

    try:
        with open(temp_path, "wb") as temp_file:
            temp_file.write(file_bytes)

        document = document_engine.process(temp_path)
        return document.raw_text or ""
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"No embedded text found, and OCR fallback failed: {exc}",
        ) from exc
    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except OSError:
            pass


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/process-invoice")
async def process_invoice(file: UploadFile = File(...)):
    """
    Processes uploaded invoice PDFs through the hybrid extraction pipeline.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF invoices are supported.")

    content = await file.read()
    raw_ocr_text = extract_text_with_ocr_fallback(content, file.filename)
    if not raw_ocr_text.strip():
        raise HTTPException(status_code=422, detail="No readable text found in the uploaded PDF after OCR.")

    return pipeline.process(raw_ocr_text)
