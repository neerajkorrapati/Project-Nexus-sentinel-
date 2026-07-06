from models.invoice import Invoice
import re


class ExtractionEngine:

    def extract(self, document):

        raw_text = document.raw_text

        invoice = Invoice()

        lines = raw_text.split("\n")

        for line in lines:

            line = line.strip()

            if invoice.vendor == "" and line:
                invoice.vendor = line

            if line.startswith("Invoice Number"):
                invoice.invoice_number = line.split(":")[1].strip()

            if line.startswith("Invoice Date"):
                invoice.invoice_date = line.split(":")[1].strip()

            if line.startswith("Subtotal"):
                value = re.findall(r"[\d.]+", line)
                if value:
                    invoice.subtotal = float(value[-1])

            if line.startswith("GST ("):
                value = re.findall(r"[\d.]+", line)
                if value:
                    invoice.gst = float(value[-1])

            if line.startswith("Grand Total"):
                value = re.findall(r"[\d.]+", line)
                if value:
                    invoice.grand_total = float(value[-1])

        return invoice