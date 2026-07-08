"""
===========================================================
Project Nexus — Shared Execution Pipeline Gateway

Core orchestration workflow engine feeding text structures 
through decoupled, reusable system optimization utilities.
===========================================================
"""

import os
from engine.document_engine import DocumentEngine
from engine.extraction_engine import ExtractionEngine
from engine.validation_engine import ValidationEngine
from engine.decision_engine import DecisionEngine

# Platform Shared Core Utility Integrations
from engine.currency_engine import CurrencyEngine
from engine.tax_engine import TaxEngine


class InvoicePipeline:

    def __init__(self):
        self.document_engine = DocumentEngine()
        self.extraction_engine = ExtractionEngine()
        self.validation_engine = ValidationEngine()
        self.decision_engine = DecisionEngine()
        
        # Instantiate platform-shared utilities safely
        self.currency_engine = CurrencyEngine()
        self.tax_engine = TaxEngine()

    async def run(self, uploaded_file):
        os.makedirs("uploads", exist_ok=True)
        file_location = os.path.join("uploads", uploaded_file.filename)

        with open(file_location, "wb") as f:
            f.write(await uploaded_file.read())

        # Step 1: Execute file parsing and read the text
        document = self.document_engine.process(file_location)

        # Step 2: Trigger the primary extraction engine layout sequence
        invoice = self.extraction_engine.extract(document)

        # Re-parse tokens to extract core system contextual intelligence
        clean_text = self.extraction_engine.normalizer.normalize(document.raw_text)
        tokens = self.extraction_engine.parser.parse(clean_text)

        # Step 3: Execute the shared platform Currency Engine
        detected_iso = self.currency_engine.detect_currency(document.raw_text, fallback_country="IN")
        invoice.currency = detected_iso
        invoice.currency_meta = {
            "iso_code": detected_iso,
            "is_domestic_currency": (detected_iso == "INR")
        }

        # Step 4: Execute the shared platform Country Tax Engine rules
        invoice.tax_breakdown = self.tax_engine.calculate_tax_breakdown(tokens, country_code="IN")
        invoice.gst = self.tax_engine.aggregate_total_tax(invoice.tax_breakdown, invoice.gst)

        # Step 5: Execute global transaction validation checks
        validation_report = self.validation_engine.validate(invoice)

        # Step 6: Route automated approval results via the Decision Engine
        decision = self.decision_engine.decide(validation_report)

        return {
            "platform_metadata": {
                "suite_version": "5.0.0",
                "ingestion_source": document.source,
                "token_stream_count": len(tokens)
            },
            "decision": decision,
            "invoice": invoice.__dict__,
            "validation": validation_report
        }