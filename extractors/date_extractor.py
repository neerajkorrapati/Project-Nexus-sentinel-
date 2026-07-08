"""
===========================================================
Invoice Agent V4

Date Extractor

Extracts canonical dates using confidence prioritization layers.
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class DateExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()

    def extract(self, tokens):
        # Heuristic 1: Prioritize explicit keyword token extractions (Confidence 1.0)
        for token in tokens:
            if token.label == "invoice_date" and token.confidence == 1.0:
                cleaned = self.utils.extract_date(token.value)
                val = cleaned if cleaned else token.value
                self.debug("Invoice Date (Explicit Anchor)", val)
                return val

        # Heuristic 2: Fall back to raw pattern regex evaluations (Confidence 0.80)
        for token in tokens:
            if token.label == "invoice_date" and token.confidence == 0.80:
                self.debug("Invoice Date (Pattern Fallback)", token.value)
                return token.value

        return ""