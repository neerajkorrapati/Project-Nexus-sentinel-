"""
===========================================================
Invoice Agent V4

GST Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor
from engine.currency_engine import CurrencyEngine


class GSTExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()
        self.currency_util = CurrencyEngine()

    def extract(self, tokens):
        candidates = []
        for token in tokens:
            if token.label == "gst":
                amount = self.currency_util.normalize_amount(token.value)
                if amount > 0:
                    candidates.append(amount)
        
        if candidates:
            final_gst = max(candidates)
            self.debug("GST Target Value Captured", final_gst)
            return final_gst
            
        return 0.0