"""
===========================================================

Invoice Agent V4

Date Extractor

Works on DocumentTokens

===========================================================
"""

from extractors.base_extractor import BaseExtractor


class DateExtractor(BaseExtractor):

    def __init__(self):

        super().__init__()

    def extract(self, tokens):

        # ------------------------------------
        # Strategy 1
        # Exact invoice_date token
        # ------------------------------------

        for token in tokens:

            if token.label == "invoice_date":
                
                # Use utils to clean/format the date if possible
                extracted_date = self.utils.extract_date(token.value)
                final_val = extracted_date if extracted_date else token.value

                self.debug("Invoice Date", final_val)

                return final_val

        # ------------------------------------
        # Strategy 2
        # Regex fallback on all tokens
        # ------------------------------------

        for token in tokens:
            
            fallback_date = self.utils.extract_date(token.value)
            
            if fallback_date:
                
                self.debug("Invoice Date (Fallback)", fallback_date)
                
                return fallback_date

        return ""