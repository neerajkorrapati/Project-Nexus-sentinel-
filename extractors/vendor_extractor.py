"""
===========================================================

Invoice Agent V4

Vendor Extractor

Works on DocumentTokens instead of raw OCR lines.

===========================================================
"""

from extractors.base_extractor import BaseExtractor


class VendorExtractor(BaseExtractor):

    def extract(self, tokens):

        # ---------------------------------------
        # Strategy 1
        # Explicit vendor token
        # ---------------------------------------

        for token in tokens:

            if token.label == "vendor":

                self.debug("Vendor", token.value)

                return token.value

        # ---------------------------------------
        # Strategy 2
        # First high-confidence text
        # ---------------------------------------

        ignore = {

            "invoice_number",

            "invoice_date",

            "subtotal",

            "grand_total",

            "gst",

            "amount"

        }

        for token in tokens:

            if token.label in ignore:

                continue

            if len(token.value.strip()) < 3:

                continue

            self.debug("Vendor (Fallback)", token.value)

            return token.value

        return ""