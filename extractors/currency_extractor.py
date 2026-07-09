"""
===========================================================
Invoice Agent V4 - Currency Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class CurrencyExtractor(BaseExtractor):

    def extract(self, tokens):
        currencies = self.tokens_by_label(tokens, "currency")
        if currencies:
            value = currencies[0].value
            self.debug("Currency", value)
            return value

        return "INR"
