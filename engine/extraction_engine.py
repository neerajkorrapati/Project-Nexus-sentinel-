import re
from models.invoice import Invoice


class ExtractionEngine:

    def extract(self, document):

        print("\n========== EXTRACTION ENGINE ==========\n")

        raw_text = document.raw_text

        invoice = Invoice()

        lines = raw_text.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            lower_line = line.lower()

            # -------------------------
            # Vendor
            # -------------------------

            if invoice.vendor == "":

                if (
                    "invoice" not in lower_line
                    and "gst" not in lower_line
                    and "date" not in lower_line
                    and "subtotal" not in lower_line
                    and "grand total" not in lower_line
                ):
                    invoice.vendor = line

            # -------------------------
            # Invoice Number
            # -------------------------

            if (
                "invoice number" in lower_line
                or "invoice no" in lower_line
                or "invoice #" in lower_line
            ):

                parts = line.split(":", 1)

                if len(parts) == 2:
                    invoice.invoice_number = parts[1].strip()

            # -------------------------
            # Invoice Date
            # -------------------------

            if "invoice date" in lower_line:

                parts = line.split(":", 1)

                if len(parts) == 2:
                    invoice.invoice_date = parts[1].strip()

            # -------------------------
            # Subtotal
            # -------------------------

            if "subtotal" in lower_line:

                values = re.findall(r"\d+\.\d+|\d+", line)

                if values:
                    invoice.subtotal = float(values[-1])

            # -------------------------
            # GST
            # -------------------------

            if (
                "gst (" in lower_line
                or "cgst" in lower_line
                or "sgst" in lower_line
                or "igst" in lower_line
            ):

                values = re.findall(r"\d+\.\d+|\d+", line)

                if values:
                    invoice.gst += float(values[-1])

            # -------------------------
            # Grand Total
            # -------------------------

            if (
                "grand total" in lower_line
                or "amount payable" in lower_line
                or "total amount" in lower_line
            ):

                values = re.findall(r"\d+\.\d+|\d+", line)

                if values:
                    invoice.grand_total = float(values[-1])

        print("\n========== EXTRACTED INVOICE ==========\n")

        print(f"Vendor          : {invoice.vendor}")
        print(f"Invoice Number  : {invoice.invoice_number}")
        print(f"Invoice Date    : {invoice.invoice_date}")
        print(f"Subtotal        : {invoice.subtotal}")
        print(f"GST             : {invoice.gst}")
        print(f"Grand Total     : {invoice.grand_total}")

        return invoice