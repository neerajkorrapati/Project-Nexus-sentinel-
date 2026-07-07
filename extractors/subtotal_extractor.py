"""
===========================================================

Invoice Agent V4

Subtotal Extractor

===========================================================
"""

from extractors.base_extractor import BaseExtractor


class SubtotalExtractor(BaseExtractor):

    def __init__(self):

        super().__init__()

    def extract(self, tokens):

        for token in tokens:

            if token.label == "subtotal":
                
                amount = self.utils.extract_number(token.value)
                
                if amount is not None:
                    
                    self.debug("Subtotal", amount)
                    
                    return amount

        return 0.0