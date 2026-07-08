"""
===========================================================
Invoice Agent V4

OCR Normalizer

Cleans predictable OCR misread structures from document text
without damaging transactional identifiers like hyphens.
===========================================================
"""

import re


class OCRNormalizer:

    def __init__(self):
        pass

    def normalize(self, text: str) -> str:
        if not text:
            return ""

        text = self.fix_common_ocr_errors(text)
        text = self.remove_extra_spaces(text)
        text = self.normalize_currency(text)

        return text

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
            "|": "|",
            "O0": "00"
        }
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)
        return text

    def remove_extra_spaces(self, text: str) -> str:
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{2,}", "\n", text)
        return text.strip()

    def normalize_currency(self, text: str) -> str:
        text = text.replace("Rs.", "₹")
        text = text.replace("Rs", "₹")
        text = text.replace("INR", "₹")
        return text