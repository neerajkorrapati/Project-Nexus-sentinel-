import io
import pdfplumber
from fastapi import FastAPI, UploadFile, File
from pipeline.invoice_pipeline import InvoicePipeline

app = FastAPI()
pipeline = InvoicePipeline()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Safely reads PDF bytes in memory and extracts text layer page by page.
    """
    text = ""
    # Load the byte stream into pdfplumber without saving to disk
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

@app.post("/process-invoice")
async def process_invoice(file: UploadFile = File(...)):
    # 1. Read the uploaded file into memory
    content = await file.read()
    
    # 2. Extract the raw text using the function defined above
    raw_ocr_text = extract_text_from_pdf(content)
    
    # 3. Pass the raw text directly to the hybrid orchestrator
    final_result = pipeline.process(raw_ocr_text)
    
    # 4. Return the fully validated JSON
    return final_result