class ValidationEngine:

    def validate(self, invoice):

        errors = []

        if invoice.vendor == "":
            errors.append("Vendor missing")

        if invoice.invoice_number == "":
            errors.append("Invoice Number missing")

        if invoice.subtotal == 0:
            errors.append("Subtotal missing")

        if invoice.gst == 0:
            errors.append("GST missing")

        if invoice.grand_total == 0:
            errors.append("Grand Total missing")

        expected = invoice.subtotal + invoice.gst

        if abs(expected - invoice.grand_total) > 0.01:
            errors.append("Total calculation incorrect")

        return {

            "passed": len(errors) == 0,

            "errors": errors

        }