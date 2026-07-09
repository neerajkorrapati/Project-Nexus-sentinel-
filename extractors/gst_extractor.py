"""
===========================================================
Invoice Agent V4 - GST Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class GSTExtractor(BaseExtractor):

    def extract(self, tokens):
        amounts = self.amounts_for_alias(tokens, "gst", max_distance=1)
        values = self.numeric_values(amounts)

        if not values:
            return 0.0

        gst = round(sum(values), 2) if len(values) > 1 else values[0]
        self.debug("GST", gst)
        return gst
