import io
import pdfplumber
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File

# Load environment variables FIRST before instantiating pipeline engines
load_dotenv()

from pipeline.invoice_pipeline import InvoicePipeline

app = FastAPI(title="Project Nexus — Invoice Processing API")
pipeline = InvoicePipeline()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Safely reads PDF bytes in memory and extracts text layer page by page.
    """
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
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