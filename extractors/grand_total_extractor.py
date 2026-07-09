"""
===========================================================
Invoice Agent V4 - Grand Total Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class GrandTotalExtractor(BaseExtractor):

    def extract(self, tokens):
        aliases = self.alias_tokens(tokens, "grand_total")

        for alias in reversed(aliases):
            values = self.numeric_values(self.tokens_on_line(tokens, "amount", alias.line_number))
            if values:
                total = max(values)
                self.debug("Grand Total", total)
                return total

        nearby_amounts = self.amounts_for_alias(tokens, "grand_total", max_distance=1)
        values = self.numeric_values(nearby_amounts)
        if values:
            total = max(values)
            self.debug("Grand Total", total)
            return total

        return 0.0
