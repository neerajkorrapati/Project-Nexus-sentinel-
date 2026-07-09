"""
===========================================================
Invoice Agent V4 - Invoice Number Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class InvoiceNumberExtractor(BaseExtractor):

    def extract(self, tokens):
        for alias in self.alias_tokens(tokens, "invoice_number"):
            same_line = self.tokens_on_line(tokens, "identifier", alias.line_number)
            next_line = self.tokens_on_line(tokens, "identifier", alias.line_number + 1)
            candidates = same_line or next_line
            if candidates:
                value = candidates[0].value
                self.debug("Invoice Number", value)
                return value

            line = self.line_text(tokens, alias.line_number)
            value = self._value_after_alias(line)
            if value:
                self.debug("Invoice Number", value)
                return value

        identifiers = self.tokens_by_label(tokens, "identifier")
        if identifiers:
            value = identifiers[0].value
            self.debug("Invoice Number Fallback", value)
            return value

        return "UNKNOWN"

    def _value_after_alias(self, line: str) -> str:
        if ":" in line:
            value = line.split(":", 1)[1].strip()
            if value:
                return value.split()[0]
        return ""
