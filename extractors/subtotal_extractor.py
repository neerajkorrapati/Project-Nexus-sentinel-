"""
===========================================================
Invoice Agent V4

Subtotal Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor
from engine.currency_engine import CurrencyEngine


class SubtotalExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()
        self.currency_util = CurrencyEngine()

    def extract(self, tokens):
        candidates = []
        for token in tokens:
            if token.label == "subtotal":
                amount = self.currency_util.normalize_amount(token.value)
                if amount > 0:
                    candidates.append(amount)
        
        if candidates:
            # Capture the maximum valid candidate to bypass table headers safely
            final_subtotal = max(candidates)
            self.debug("Subtotal Target Value Captured", final_subtotal)
            return final_subtotal
            
        return 0.0