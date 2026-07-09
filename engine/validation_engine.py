"""
===========================================================
Project Nexus — Validation Engine

Performs mathematical cross-checks on the extracted data.
Subtotal + GST == Grand Total
===========================================================
"""


class ValidationEngine:

    def validate(self, invoice_data: dict) -> dict:
        if not isinstance(invoice_data, dict):
            invoice_data = invoice_data.__dict__

        errors = []
        
        subtotal = float(invoice_data.get("subtotal", 0.0) or 0.0)
        gst = float(invoice_data.get("gst", 0.0) or 0.0)
        grand_total = float(invoice_data.get("grand_total", 0.0) or 0.0)

        # Ensure essential totals are present
        if subtotal <= 0:
            errors.append("Subtotal missing or indicates a negative/zero balance.")
        if grand_total <= 0:
            errors.append("Grand Total valuation metric missing or invalid.")

        # Financial Cross-Check (allowing a small rounding tolerance of 0.05)
        calculated_total = round(subtotal + gst, 2)
        actual_total = round(grand_total, 2)

        if abs(calculated_total - actual_total) > 0.05:
            errors.append(
                f"Financial Calculation Mismatch: Calculated balance ({calculated_total:.2f}) "
                f"does not balance with Grand Total entry ({actual_total:.2f})."
            )

        passed = len(errors) == 0
        return {
            "passed": passed,
            "errors": errors
        }
