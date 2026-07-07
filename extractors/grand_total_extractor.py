"""
===========================================================

Invoice Agent V4

Grand Total Extractor

===========================================================
"""

from extractors.base_extractor import BaseExtractor


class GrandTotalExtractor(BaseExtractor):

    def __init__(self):

        super().__init__()

    def extract(self, tokens):

        for token in tokens:

            if token.label == "grand_total":
                
                amount = self.utils.extract_number(token.value)
                
                if amount is not None:
                    
                    self.debug("Grand Total", amount)
                    
                    return amount

        return 0.0