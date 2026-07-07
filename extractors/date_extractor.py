"""
===========================================================

Invoice Agent V3.5

Invoice Number Extractor

Works on DocumentTokens

===========================================================
"""

import re

from extractors.base_extractor import BaseExtractor


class InvoiceNumberExtractor(BaseExtractor):

    def __init__(self):

        super().__init__()

    def extract(self, tokens):

        # ------------------------------------
        # Strategy 1
        # Exact invoice_number token
        # ------------------------------------

        for token in tokens:

            if token.label == "invoice_number":

                self.debug("Invoice Number", token.value)

                return token.value

        # ------------------------------------
        # Strategy 2
        # Regex fallback
        # ------------------------------------

        patterns = [

            r"[A-Za-z]{2,}[-/]\d+",

            r"\d{4}-\d{2}/\d+",

            r"[A-Za-z0-9/-]{6,}"

        ]

        for token in tokens:

            for pattern in patterns:

                match = re.search(pattern, token.value)

                if match:

                    value = match.group()

                    self.debug("Invoice Number (Regex)", value)

                    return value

        return ""