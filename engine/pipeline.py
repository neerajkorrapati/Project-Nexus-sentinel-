import os

from engine.document_engine import DocumentEngine
from engine.extraction_engine import ExtractionEngine
# ValidationEngine is implemented below in this same file
from engine.decision_engine import DecisionEngine


class InvoicePipeline:

    def __init__(self):

        self.document_engine = DocumentEngine()

        self.extraction_engine = ExtractionEngine()

        self.validation_engine = ValidationEngine()

        self.decision_engine = DecisionEngine()

    async def run(self, uploaded_file):

        os.makedirs("uploads", exist_ok=True)

        file_location = os.path.join(
            "uploads",
            uploaded_file.filename
        )

        with open(file_location, "wb") as f:
            f.write(await uploaded_file.read())

        print("\n========== RAW TEXT ==========\n")

        document = self.document_engine.process(file_location)

        print("\n========== DOCUMENT ==========\n")

        print("\n========================")
        print("DOCUMENT")
        print("========================")

        print("Source :", document.source)
        print("Pages  :", document.page_count)
        print("Confidence :", document.confidence)

        print("\n========================")
        print("RAW TEXT")
        print("========================")

        print(document.raw_text)

        invoice = self.extraction_engine.extract(document)

        validation = self.validation_engine.validate(invoice)

        decision = self.decision_engine.decide(validation)

        return {

            "decision": decision,

            "invoice": invoice.__dict__,

            "validation": validation

        }

class ValidationEngine:

    def validate(self, invoice):

        errors = []

        if invoice.vendor == "":
            errors.append("Vendor missing")

        if invoice.invoice_number == "":
            errors.append("Invoice Number missing")

        if invoice.subtotal == 0:
            errors.append("Subtotal missing")

        if invoice.gst == 0:
            errors.append("GST missing")

        if invoice.grand_total == 0:
            errors.append("Grand Total missing")

        expected = invoice.subtotal + invoice.gst

        if abs(expected - invoice.grand_total) > 0.01:
            errors.append("Total calculation incorrect")

        return {

            "passed": len(errors) == 0,

            "errors": errors

        }