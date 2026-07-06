from fastapi import FastAPI, UploadFile, File

from engine.pipeline import InvoicePipeline

app = FastAPI(title="Invoice Automation Engine")

pipeline = InvoicePipeline()


@app.get("/")
def home():

    return {

        "message": "Invoice Automation Engine Running"

    }


@app.post("/process")
async def process_invoice(file: UploadFile = File(...)):

    result = await pipeline.run(file)

    return result