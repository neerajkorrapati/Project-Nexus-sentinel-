"""
===========================================================
Invoice Agent V4 - Date Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class DateExtractor(BaseExtractor):

    def extract(self, tokens):
        for alias in self.alias_tokens(tokens, "invoice_date"):
            same_line = self.tokens_on_line(tokens, "date", alias.line_number)
            next_line = self.tokens_on_line(tokens, "date", alias.line_number + 1)
            candidates = same_line or next_line
            if candidates:
                value = candidates[0].value
                self.debug("Invoice Date", value)
                return value

        dates = self.tokens_by_label(tokens, "date")
        if dates:
            value = dates[0].value
            self.debug("Invoice Date Fallback", value)
            return value

        return "UNKNOWN"
