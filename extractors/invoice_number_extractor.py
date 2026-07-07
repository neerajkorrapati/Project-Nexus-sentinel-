"""
===========================================================
Invoice Agent V3

Invoice Number Extractor

Responsible only for extracting
the invoice number.

Author : Project Nexus
===========================================================
"""

import re

from extractors.base_extractor import BaseExtractor


class InvoiceNumberExtractor(BaseExtractor):

    def __init__(self):

        super().__init__()

    def extract(self, lines):

        aliases = self.aliases("invoice_number")

        # -------------------------------------------------
        # Strategy 1
        # Find line containing alias
        # -------------------------------------------------

        for index, line in enumerate(lines):

            if self.utils.contains_alias(line, aliases):

                # -----------------------------
                # Invoice Number: INV001
                # -----------------------------

                value = self.after_colon(line)

                if value:

                    self.debug("Invoice Number", value)

                    return value

                # -----------------------------
                # Invoice Number
                # INV001
                # -----------------------------

                next_line = self.utils.next_non_empty(lines, index)

                if next_line:

                    self.debug("Invoice Number", next_line)

                    return next_line

        # -------------------------------------------------
        # Strategy 2
        # Regex fallback
        # -------------------------------------------------

        patterns = [

            r"[A-Z]{2,}[-/]?\d+",
            r"\d{4}-\d{2}/\d+",
            r"\d+/\d+/\d+",
            r"[A-Za-z0-9/-]{5,}"

        ]

        for line in lines:

            for pattern in patterns:

                match = re.search(pattern, line)

                if match:

                    value = match.group()

                    self.debug("Invoice Number (Regex)", value)

                    return value

        return ""