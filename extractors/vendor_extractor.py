"""
===========================================================
Invoice Agent V4

Vendor Extractor

Identifies the vendor using corporate designator priority matches.
===========================================================
"""

import re
from extractors.base_extractor import BaseExtractor


class VendorExtractor(BaseExtractor):

    def extract(self, tokens):
        # Strategy 1: Explicit vendor label mapping matches with structural verification guards
        for token in tokens:
            if token.label == "vendor" and token.confidence == 1.0:
                val_clean = token.value.strip()
                
                # Guard: Reject false-positive lines containing registration tax attributes
                if any(k in val_clean.lower() for k in ["gst", "gstin", "pan", "vat", "tax id", "tax no"]):
                    continue
                if re.search(r"\d{4,}", val_clean):  # Rejects registration IDs, serials, and phone blocks
                    continue
                    
                self.debug("Vendor Name Found", val_clean)
                return val_clean

        # Strategy 2: Legal Corporate Suffix Heuristic Scan
        raw_blocks = [t for t in tokens if t.label == "raw_text_block"]
        raw_blocks.sort(key=lambda x: x.line_number)

        corporate_suffixes = [r"\bpvt\b", r"\bltd\b", r"\binc\b", r"\bcorp\b", r"\benterprises\b", r"\blimited\b"]
        
        # High-Confidence Pass: Look for standard corporate indicators in the top header blocks
        for token in raw_blocks[:6]:
            val = token.value.strip()
            val_lower = val.lower()
            
            if any(re.search(suffix, val_lower) for suffix in corporate_suffixes):
                self.debug("Vendor Identity (Legal Suffix Heuristic Matching)", val)
                return val

        # Strategy 3: Top-Down Clean Banner Fallback
        buyer_indicators = ["bill to", "ship to", "client", "customer", "buyer", "receiver", "name:", "party"]
        meta_indicators = ["invoice", "date", "reverse", "state", "mobile", "gstin", "tax", "original", "transport", "vehicle"]
        address_indicators = ["s.no", "plot", "floor", "street", "road", "ward", "bldg", "avenue", "lane", "box", "plot no"]

        for token in raw_blocks:
            val = token.value.strip()
            val_lower = val.lower()

            if any(ind in val_lower for ind in buyer_indicators):
                continue
            if any(ind in val_lower for ind in meta_indicators):
                continue
            if any(ind in val_lower for ind in address_indicators):
                continue
            if re.search(r"\d{4,}", val):
                continue
            if len(val) < 3:
                continue

            self.debug("Vendor (Top-Down Banner Line Fallback)", val)
            return val

        return ""