import re

from models.invoice import Invoice


class ExtractionEngine:

    def extract(self, raw_text: str):

        invoice = Invoice()

        vendor_match = re.search(r"^(.*)", raw_text)
        invoice_match = re.search(r"Invoice Number:\s*(.*)", raw_text)
        date_match = re.search(r"Invoice Date:\s*(.*)", raw_text)
        subtotal_match = re.search(r"Subtotal\s+([\d.]+)", raw_text)
        gst_match = re.search(r"GST.*?([\d.]+)", raw_text)
        total_match = re.search(r"Grand Total\s+([\d.]+)", raw_text)

        if vendor_match:
            invoice.vendor = vendor_match.group(1).strip()

        if invoice_match:
            invoice.invoice_number = invoice_match.group(1).strip()

        if date_match:
            invoice.invoice_date = date_match.group(1).strip()

        if subtotal_match:
            invoice.subtotal = float(subtotal_match.group(1))

        if gst_match:
            invoice.gst = float(gst_match.group(1))

        if total_match:
            invoice.grand_total = float(total_match.group(1))

        return invoice