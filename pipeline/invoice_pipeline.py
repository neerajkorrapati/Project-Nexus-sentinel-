"""
===========================================================
Project Nexus Sentinel - Invoice Processing Pipeline
===========================================================
"""

from engine.ai_engine import AIEngine
from engine.validation_engine import ValidationEngine
from extractors.currency_extractor import CurrencyExtractor
from extractors.date_extractor import DateExtractor
from extractors.grand_total_extractor import GrandTotalExtractor
from extractors.gst_extractor import GSTExtractor
from extractors.invoice_number_extractor import InvoiceNumberExtractor
from extractors.subtotal_extractor import SubtotalExtractor
from extractors.vendor_extractor import VendorExtractor
from parser.document_parser import DocumentParser


class InvoicePipeline:

    def __init__(self):
        self.parser = DocumentParser()
        self.validator = ValidationEngine()
        self.ai_engine = AIEngine()
        self.vendor_extractor = VendorExtractor()
        self.invoice_number_extractor = InvoiceNumberExtractor()
        self.date_extractor = DateExtractor()
        self.currency_extractor = CurrencyExtractor()
        self.subtotal_extractor = SubtotalExtractor()
        self.gst_extractor = GSTExtractor()
        self.grand_total_extractor = GrandTotalExtractor()

    def process(self, raw_ocr_text: str) -> dict:
        tokens = self.parser.parse(raw_ocr_text)

        deterministic_data = {
            "vendor": self.vendor_extractor.extract(tokens),
            "invoice_number": self.invoice_number_extractor.extract(tokens),
            "invoice_date": self.date_extractor.extract(tokens),
            "currency": self.currency_extractor.extract(tokens),
            "subtotal": self.subtotal_extractor.extract(tokens),
            "gst": self.gst_extractor.extract(tokens),
            "grand_total": self.grand_total_extractor.extract(tokens),
        }
        self._repair_financials(deterministic_data, tokens)

        validation_results = self.validator.validate(deterministic_data)
        if validation_results.get("passed", False):
            return self._build_response(deterministic_data, validation_results, "DETERMINISTIC_RULES")

        print("[Pipeline] Deterministic validation failed. Escalating to AI rectification...")
        rectified_data = self.ai_engine.rectify_extraction(raw_ocr_text, deterministic_data)
        ai_validation_results = self.validator.validate(rectified_data)

        return self._build_response(rectified_data, ai_validation_results, "AI_RECTIFICATION_FALLBACK")

    def _build_response(self, data: dict, validation: dict, source: str) -> dict:
        return {
            "platform_metadata": {
                "suite_version": "5.5.0",
                "ingestion_source": source,
            },
            "decision": "APPROVED" if validation.get("passed", False) else "NEEDS REVIEW",
            "invoice": data,
            "validation": validation,
        }

    def _repair_financials(self, data: dict, tokens: list) -> None:
        subtotal = float(data.get("subtotal", 0.0) or 0.0)
        gst = float(data.get("gst", 0.0) or 0.0)
        grand_total = float(data.get("grand_total", 0.0) or 0.0)

        amount_candidates = []
        for token in tokens:
            if token.label != "amount":
                continue

            raw = token.raw_text.lower()
            if any(skip in raw for skip in ["mobile", "phone", "gstin", "state code"]):
                continue

            try:
                value = float(token.value)
            except (TypeError, ValueError):
                continue

            if 0 < value < 10000000:
                amount_candidates.append(value)

        if subtotal > 0 and amount_candidates and grand_total <= subtotal:
            data["grand_total"] = max(amount_candidates)
            grand_total = data["grand_total"]

        expected_gst = round(grand_total - subtotal, 2)
        current_total = round(subtotal + gst, 2)

        if subtotal > 0 and grand_total > subtotal and abs(current_total - grand_total) > 0.05:
            data["gst"] = expected_gst
