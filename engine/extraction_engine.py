"""
===========================================================
Invoice Agent V4 - Extraction Engine

Coordinates parsing and field extractors for document-engine workflows.
===========================================================
"""

from extractors.currency_extractor import CurrencyExtractor
from extractors.date_extractor import DateExtractor
from extractors.grand_total_extractor import GrandTotalExtractor
from extractors.gst_extractor import GSTExtractor
from extractors.invoice_number_extractor import InvoiceNumberExtractor
from extractors.subtotal_extractor import SubtotalExtractor
from extractors.vendor_extractor import VendorExtractor
from models.invoice import Invoice
from normalizer.ocr_normalizer import OCRNormalizer
from parser.document_parser import DocumentParser


class ExtractionEngine:

    def __init__(self):
        self.normalizer = OCRNormalizer()
        self.parser = DocumentParser()
        self.vendor = VendorExtractor()
        self.invoice_number = InvoiceNumberExtractor()
        self.date = DateExtractor()
        self.currency = CurrencyExtractor()
        self.subtotal = SubtotalExtractor()
        self.gst = GSTExtractor()
        self.grand_total = GrandTotalExtractor()

    def extract(self, document):
        clean_text = self.normalizer.normalize(document.raw_text)
        tokens = self.parser.parse(clean_text)

        invoice = Invoice()
        invoice.vendor = self.vendor.extract(tokens)
        invoice.invoice_number = self.invoice_number.extract(tokens)
        invoice.invoice_date = self.date.extract(tokens)
        invoice.currency = self.currency.extract(tokens)
        invoice.subtotal = self.subtotal.extract(tokens)
        invoice.gst = self.gst.extract(tokens)
        invoice.grand_total = self.grand_total.extract(tokens)

        return invoice
