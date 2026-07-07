"""
===========================================================
Invoice Agent V3

Date Extractor

Responsible only for extracting
the invoice date.

Author : Project Nexus
===========================================================
"""

import re

from extractors.base_extractor import BaseExtractor


class DateExtractor(BaseExtractor):

    def __init__(self):

        super().__init__()

    def extract(self, lines):

        aliases = self.aliases("invoice_date")

        # -------------------------------------------------
        # Strategy 1
        # Search using aliases
        # -------------------------------------------------

        for index, line in enumerate(lines):

            if self.utils.contains_alias(line, aliases):

                # -----------------------------
                # Invoice Date: 01/08/2017
                # -----------------------------

                value = self.after_colon(line)

                if value:

                    date = self.date(value)

                    if date:

                        self.debug("Invoice Date", date)

                        return date

                # -----------------------------
                # Invoice Date
                # 01/08/2017
                # -----------------------------

                next_line = self.utils.next_non_empty(lines, index)

                if next_line:

                    date = self.date(next_line)

                    if date:

                        self.debug("Invoice Date", date)

                        return date

        # -------------------------------------------------
        # Strategy 2
        # Regex fallback
        # -------------------------------------------------

        patterns = [

            r"\d{2}/\d{2}/\d{4}",
            r"\d{2}-\d{2}-\d{4}",
            r"\d{4}/\d{2}/\d{2}",
            r"\d{4}-\d{2}-\d{2}"

        ]

        for line in lines:

            for pattern in patterns:

                match = re.search(pattern, line)

                if match:

                    date = match.group()

                    self.debug("Invoice Date (Regex)", date)

                    return date

        return ""