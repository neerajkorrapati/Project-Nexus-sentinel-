import os

from engine.document_engine import DocumentEngine
from engine.extraction_engine import ExtractionEngine
from engine.validation_engine import ValidationEngine
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

        print(document)

        invoice = self.extraction_engine.extract(document)

        validation = self.validation_engine.validate(invoice)

        decision = self.decision_engine.decide(validation)

        return {

            "decision": decision,

            "invoice": invoice.__dict__,

            "validation": validation

        }