"""
===========================================================
Project Nexus - Vendor Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class VendorExtractor(BaseExtractor):

    HEADER_EXCLUSIONS = {
        "tax invoice",
        "invoice",
        "original for recipient",
        "duplicate for supplier",
        "bill of supply",
    }

    def extract(self, tokens: list) -> str:
        vendor_aliases = self.alias_tokens(tokens, "vendor")
        for alias in vendor_aliases:
            line = self.line_text(tokens, alias.line_number)
            candidate = self._value_after_alias(line)
            if candidate:
                self.debug("Vendor Identified", candidate)
                return candidate

        for token in self.line_tokens(tokens)[:12]:
            line = token.value.strip()
            normalized = line.lower()
            if normalized in self.HEADER_EXCLUSIONS:
                continue
            if self.tokens_on_line(tokens, "field_alias", token.line_number):
                continue
            if self.tokens_on_line(tokens, "amount", token.line_number):
                continue
            if len(line) >= 3:
                self.debug("Vendor Identified", line)
                return line

        return "UNKNOWN_VENDOR"

    def _value_after_alias(self, line: str) -> str:
        if ":" in line:
            value = line.split(":", 1)[1].strip()
            if value:
                return value
        return ""
