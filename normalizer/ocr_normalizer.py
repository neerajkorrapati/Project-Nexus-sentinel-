"""
===========================================================
Invoice Agent V3

OCR Normalizer

Purpose:
--------

OCR output is rarely perfect.

Example:

Invo1ce
Grand TotaI
Sub Tota1
GST :
Net Arnount

This module cleans OCR mistakes before extraction.

===========================================================
"""

import re


class OCRNormalizer:

    def __init__(self):
        pass

    # ----------------------------------------------------
    # Main Entry
    # ----------------------------------------------------

    def normalize(self, text: str) -> str:

        if not text:
            return ""

        text = self.fix_common_ocr_errors(text)

        text = self.remove_extra_spaces(text)

        text = self.normalize_currency(text)

        text = self.normalize_dates(text)

        return text

    # ----------------------------------------------------
    # OCR Character Fixes
    # ----------------------------------------------------

    def fix_common_ocr_errors(self, text: str) -> str:

        replacements = {

            "Invo1ce": "Invoice",
            "Inv0ice": "Invoice",

            "TotaI": "Total",
            "Sub Tota1": "Subtotal",

            "Arnount": "Amount",
            "arnount": "amount",

            "GST :": "GST:",
            "GST ;": "GST:",

            "|": "I",

            "O0": "00"

        }

        for wrong, correct in replacements.items():

            text = text.replace(wrong, correct)

        return text

    # ----------------------------------------------------
    # Remove Extra Spaces
    # ----------------------------------------------------

    def remove_extra_spaces(self, text: str) -> str:

        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(r"\n{2,}", "\n", text)

        return text.strip()

    # ----------------------------------------------------
    # Currency Formatting
    # ----------------------------------------------------

    def normalize_currency(self, text: str) -> str:

        text = text.replace("Rs.", "₹")
        text = text.replace("Rs", "₹")
        text = text.replace("INR", "₹")

        return text

    # ----------------------------------------------------
    # Date Formatting
    # ----------------------------------------------------

    def normalize_dates(self, text: str) -> str:

        text = text.replace("-", "/")

        return text