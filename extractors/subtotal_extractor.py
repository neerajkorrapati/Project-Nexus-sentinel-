"""
===========================================================
Invoice Agent V4 - Subtotal Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class SubtotalExtractor(BaseExtractor):

    def extract(self, tokens):
        amounts = self.amounts_for_alias(tokens, "subtotal", max_distance=1)
        values = self.numeric_values(amounts)

        if values:
            subtotal = values[-1]
            self.debug("Subtotal", subtotal)
            return subtotal

        return 0.0
