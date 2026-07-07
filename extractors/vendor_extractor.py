"""
===========================================================
Invoice Agent V3

Vendor Extractor

Responsible only for extracting the vendor/company name.

Author : Project Nexus
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class VendorExtractor(BaseExtractor):

    def __init__(self):

        super().__init__()

    def extract(self, lines):

        """
        Strategy

        1. Look for explicit vendor aliases
        2. Return value after ':'
        3. Otherwise use first meaningful line
        """

        # -------------------------------------------------
        # Strategy 1
        # Explicit aliases
        # -------------------------------------------------

        aliases = self.aliases("vendor")

        for line in lines:

            if self.utils.contains_alias(line, aliases):

                value = self.after_colon(line)

                if value:

                    self.debug("Vendor (Alias)", value)

                    return value

        # -------------------------------------------------
        # Strategy 2
        # First meaningful line
        # -------------------------------------------------

        ignore_words = [

            "invoice",
            "tax invoice",
            "bill",
            "date",
            "gst",
            "subtotal",
            "grand total",
            "amount",
            "quantity",
            "qty",
            "price",
            "description"

        ]

        for line in lines:

            line = line.strip()

            if line == "":
                continue

            lower = line.lower()

            ignore = False

            for word in ignore_words:

                if word in lower:

                    ignore = True
                    break

            if ignore:
                continue

            if len(line) < 3:
                continue

            self.debug("Vendor (Fallback)", line)

            return line

        return ""