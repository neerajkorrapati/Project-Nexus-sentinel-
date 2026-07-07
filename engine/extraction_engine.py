"""
===========================================================

Invoice Agent V3.5

Extraction Engine

Coordinates the complete extraction pipeline.

===========================================================
"""

from models.invoice import Invoice

from normalizer.ocr_normalizer import OCRNormalizer
from parser.document_parser import DocumentParser

from extractors.vendor_extractor import VendorExtractor
from extractors.invoice_number_extractor import InvoiceNumberExtractor
from extractors.date_extractor import DateExtractor


class ExtractionEngine:

    def __init__(self):

        self.normalizer = OCRNormalizer()

        self.parser = DocumentParser()

        self.vendor = VendorExtractor()

        self.invoice_number = InvoiceNumberExtractor()

        self.date = DateExtractor()

    def extract(self, document):

        print("\n========== EXTRACTION ENGINE ==========\n")

        # ------------------------------------
        # OCR Normalization
        # ------------------------------------

        clean_text = self.normalizer.normalize(
            document.raw_text
        )

        # ------------------------------------
        # Parse into DocumentTokens
        # ------------------------------------

        tokens = self.parser.parse(clean_text)

        self.parser.print_tokens(tokens)

        # ------------------------------------
        # Build Invoice
        # ------------------------------------

        invoice = Invoice()

        invoice.vendor = self.vendor.extract(tokens)

        invoice.invoice_number = self.invoice_number.extract(tokens)

        invoice.invoice_date = self.date.extract(tokens)

        return invoice