"""
===========================================================
Project Nexus — Invoice Processing Pipeline

Orchestrates the Hybrid Parsing Strategy.
Tier 1: Deterministic Engine (Free, Instant)
Tier 2: Validation Gate
Tier 3: AI Escalation Engine (API Call)
===========================================================
"""

from parser.document_parser import DocumentParser
from engine.validation_engine import ValidationEngine
from engine.ai_engine import AIEngine
# Import your extractors here...

class InvoicePipeline:
    def __init__(self):
        self.parser = DocumentParser()
        self.validator = ValidationEngine()
        self.ai_engine = AIEngine()
        # self.vendor_extractor = VendorExtractor() ... etc.

    def process(self, raw_ocr_text: str) -> dict:
        # ---------------------------------------------------------
        # TIER 1: The Deterministic Pass (Cost: $0.00)
        # ---------------------------------------------------------
        tokens = self.parser.parse(raw_ocr_text)
        
        # Extract values using your current BaseExtractor logic
        deterministic_data = {
            # Example mapping; use your actual extractor instances
            "vendor": "Extracted Vendor", 
            "invoice_number": "Extracted Invoice",
            "invoice_date": "Extracted Date",
            "subtotal": 0.0,      # Hypothetically failed extraction
            "gst": 0.0,           # Hypothetically failed extraction
            "grand_total": 0.0    # Hypothetically failed extraction
        }

        # ---------------------------------------------------------
        # TIER 2: The Efficiency Gate
        # ---------------------------------------------------------
        validation_results = self.validator.validate(deterministic_data)

        if validation_results.get("passed", False):
            # If the math balances, immediately return the payload. API is bypassed.
            return self._build_response(deterministic_data, validation_results, "DETERMINISTIC_RULES")

        # ---------------------------------------------------------
        # TIER 3: The AI Escalation Layer
        # ---------------------------------------------------------
        print("[Pipeline] Validation failed. Escalating to Gemini AI Layer...")
        
        # Token Compression: Strip blank lines and excess whitespace before sending to save API costs
        compressed_text = "\n".join([line.strip() for line in raw_ocr_text.split("\n") if line.strip()])
        
        # Rectify the payload
        rectified_data = self.ai_engine.rectify_extraction(compressed_text, deterministic_data)
        
        # Re-validate the AI's math to ensure absolute accounting safety
        ai_validation_results = self.validator.validate(rectified_data)
        
        return self._build_response(rectified_data, ai_validation_results, "AI_RECTIFICATION_FALLBACK")

    def _build_response(self, data: dict, validation: dict, source: str) -> dict:
        """Constructs the final standardized enterprise JSON payload."""
        return {
            "platform_metadata": {
                "suite_version": "5.5.0",
                "ingestion_source": source
            },
            "decision": "APPROVED" if validation.get("passed", False) else "NEEDS REVIEW",
            "invoice": data,
            "validation": validation
        }