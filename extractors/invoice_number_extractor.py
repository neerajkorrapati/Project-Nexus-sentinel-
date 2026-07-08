"""
===========================================================
Invoice Agent V4

Invoice Number Extractor

Extracts canonical numbers using confidence prioritization layers.
===========================================================
"""

import re
from extractors.base_extractor import BaseExtractor


class InvoiceNumberExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()

    def extract(self, tokens):
        # Strict internal regex evaluation expressions to safeguard extraction rules
        validation_patterns = [
            r"[A-Za-z0-9]+[-/]\d+[-/][A-Za-z0-9]+",
            r"[A-Za-z0-9]+[-/]\d+",
            r"\d{4}-\d{2}/\d+"
        ]

        # Heuristic 1: Prioritize explicit keyword token extractions (Confidence 1.0)
        for token in tokens:
            if token.label == "invoice_number" and token.confidence == 1.0:
                for pattern in validation_patterns:
                    match = re.search(pattern, token.value)
                    if match:
                        self.debug("Invoice Number (Explicit Anchor)", match.group())
                        return match.group()
                
                self.debug("Invoice Number (Explicit Anchor Fallback)", token.value)
                return token.value

        # Heuristic 2: Fall back to raw pattern regex evaluations (Confidence 0.80)
        for token in tokens:
            if token.label == "invoice_number" and token.confidence == 0.80:
                self.debug("Invoice Number (Pattern Fallback)", token.value)
                return token.value

        return ""