"""
===========================================================
Invoice Agent V3

Extraction Engine

Author : Project Nexus

This engine coordinates all extractors.

Workflow

Document
    ↓
OCR Normalizer
    ↓
VendorExtractor
InvoiceNumberExtractor
DateExtractor
    ↓
Invoice Object
===========================================================
"""

from models.invoice import Invoice

from normalizer.ocr_normalizer import OCRNormalizer

from extractors.vendor_extractor import VendorExtractor
from extractors.invoice_number_extractor import InvoiceNumberExtractor
from extractors.date_extractor import DateExtractor


class ExtractionEngine:

    def __init__(self):

        self.normalizer = OCRNormalizer()

        self.vendor_extractor = VendorExtractor()

        self.invoice_number_extractor = InvoiceNumberExtractor()

        self.date_extractor = DateExtractor()

    def extract(self, document):

        print("\n========== EXTRACTION ENGINE ==========\n")

        # ----------------------------------------
        # Normalize OCR Text
        # ----------------------------------------

        clean_text = self.normalizer.normalize(
            document.raw_text
        )

        lines = clean_text.split("\n")

        invoice = Invoice()

        # ----------------------------------------
        # Run Individual Extractors
        # ----------------------------------------

        invoice.vendor = self.vendor_extractor.extract(lines)

        invoice.invoice_number = (
            self.invoice_number_extractor.extract(lines)
        )

        invoice.invoice_date = (
            self.date_extractor.extract(lines)
        )

        # ----------------------------------------
        # Debug
        # ----------------------------------------

        print("\n========== EXTRACTED ==========\n")

        print(f"Vendor          : {invoice.vendor}")

        print(f"Invoice Number  : {invoice.invoice_number}")

        print(f"Invoice Date    : {invoice.invoice_date}")

        print(f"Subtotal        : {invoice.subtotal}")

        print(f"GST             : {invoice.gst}")

        print(f"Grand Total     : {invoice.grand_total}")

        return invoice