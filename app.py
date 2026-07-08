import io
import pdfplumber
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File

# MUST BE CALLED FIRST to load API Keys into os.environ
load_dotenv()

from pipeline.invoice_pipeline import InvoicePipeline

app = FastAPI(title="Project Nexus Sentinel — Enterprise Invoice API")
pipeline = InvoicePipeline()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Reads PDF bytes with explicit layout preservation to prevent 
    column boundary collapsing during OCR parsing.
    """
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text(layout=True)
            if not extracted or not extracted.strip():
                extracted = page.extract_text(layout=False) or ""
            text += extracted + "\n"
    return text


@app.post("/process-invoice")
async def process_invoice(file: UploadFile = File(...)):
    """
    Processes uploaded invoice PDFs through the hybrid extraction pipeline.
    """
    content = await file.read()
    raw_ocr_text = extract_text_from_pdf(content)
    final_result = pipeline.process(raw_ocr_text)
    return final_result