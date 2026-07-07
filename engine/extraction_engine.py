"""
===========================================================

Invoice Agent V4

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
from extractors.subtotal_extractor import SubtotalExtractor
from extractors.gst_extractor import GSTExtractor
from extractors.grand_total_extractor import GrandTotalExtractor


class ExtractionEngine:

    def __init__(self):

        self.normalizer = OCRNormalizer()

        self.parser = DocumentParser()

        self.vendor = VendorExtractor()

        self.invoice_number = InvoiceNumberExtractor()

        self.date = DateExtractor()
        
        self.subtotal = SubtotalExtractor()
        
        self.gst = GSTExtractor()
        
        self.grand_total = GrandTotalExtractor()

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
        
        invoice.subtotal = self.subtotal.extract(tokens)
        
        invoice.gst = self.gst.extract(tokens)
        
        invoice.grand_total = self.grand_total.extract(tokens)

        return invoice