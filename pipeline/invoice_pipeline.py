"""
===========================================================
Project Nexus Sentinel — Invoice Processing Pipeline
===========================================================
"""

from parser.document_parser import DocumentParser
from engine.validation_engine import ValidationEngine
from engine.ai_engine import AIEngine
from extractors.vendor_extractor import VendorExtractor
from extractors.subtotal_extractor import SubtotalExtractor
from extractors.gst_extractor import GSTExtractor
from extractors.grand_total_extractor import GrandTotalExtractor


class InvoicePipeline:

    def __init__(self):
        self.parser = DocumentParser()
        self.validator = ValidationEngine()
        self.ai_engine = AIEngine()
        self.vendor_extractor = VendorExtractor()
        self.subtotal_extractor = SubtotalExtractor()
        self.gst_extractor = GSTExtractor()
        self.grand_total_extractor = GrandTotalExtractor()

    def process(self, raw_ocr_text: str) -> dict:
        # Pass 1: Local Deterministic Engine (Cost: $0.00)
        tokens = self.parser.parse(raw_ocr_text)

        inv_no = next((t.value for t in tokens if t.label == "invoice_number"), "UNKNOWN")
        inv_date = next((t.value for t in tokens if t.label == "invoice_date"), "UNKNOWN")

        deterministic_data = {
            "vendor": self.vendor_extractor.extract(tokens),
            "invoice_number": inv_no,
            "invoice_date": inv_date,
            "subtotal": self.subtotal_extractor.extract(tokens),
            "gst": self.gst_extractor.extract(tokens),
            "grand_total": self.grand_total_extractor.extract(tokens)
        }

        validation_results = self.validator.validate(deterministic_data)

        # Gate Check: If math balances locally, skip AI entirely
        if validation_results.get("passed", False):
            return self._build_response(deterministic_data, validation_results, "DETERMINISTIC_RULES")

        # Escalate to Gemini AI to rectify broken math
        print("[Pipeline] Deterministic validation failed. Escalating to AI Rectification...")
        rectified_data = self.ai_engine.rectify_extraction(raw_ocr_text, deterministic_data)
        
        # Final safety check on AI output
        ai_validation_results = self.validator.validate(rectified_data)

        return self._build_response(rectified_data, ai_validation_results, "AI_RECTIFICATION_FALLBACK")

    def _build_response(self, data: dict, validation: dict, source: str) -> dict:
        return {
            "platform_metadata": {
                "suite_version": "5.5.0",
                "ingestion_source": source
            },
            "decision": "APPROVED" if validation.get("passed", False) else "NEEDS REVIEW",
            "invoice": data,
            "validation": validation
        }