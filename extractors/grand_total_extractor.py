"""
===========================================================
Invoice Agent V4

Grand Total Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor
from engine.currency_engine import CurrencyEngine


class GrandTotalExtractor(BaseExtractor):

    def __init__(self):
        super().__init__()
        self.currency_util = CurrencyEngine()

    def extract(self, tokens):
        candidates = []
        for token in tokens:
            if token.label == "grand_total":
                amount = self.currency_util.normalize_amount(token.value)
                if amount > 0:
                    candidates.append(amount)
                    
        if candidates:
            final_total = max(candidates)
            self.debug("Grand Total Target Value Captured", final_total)
            return final_total
            
        return 0.0