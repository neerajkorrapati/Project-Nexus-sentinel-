"""
===========================================================
Project Nexus — Vendor Extractor
===========================================================
"""

from extractors.base_extractor import BaseExtractor


class VendorExtractor(BaseExtractor):

    def extract(self, tokens: list) -> str:
        # Pull candidate vendor names from header raw_text_blocks
        for token in tokens:
            if token.label == "raw_text_block":
                val = token.value.strip()
                # Exclude known title header lines
                if val.lower() not in ["tax invoice", "invoice", "original for recipient"]:
                    self.debug("Vendor Identified", val)
                    return val
        return "UNKNOWN_VENDOR"