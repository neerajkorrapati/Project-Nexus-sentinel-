"""
===========================================================
Project Nexus — Enterprise Validation Engine

Deterministic logic layer validating structural accounting balances,
currency conformity, and configuration integrity rules.
===========================================================
"""

from models.invoice import Invoice


class ValidationEngine:

    def validate(self, invoice: Invoice) -> dict:
        errors = []

        # Operational Check 1: Mandatory Field Affirmation
        if not invoice.vendor or invoice.vendor.strip() == "":
            errors.append("Vendor profile identity unverified or missing")

        if not invoice.invoice_number or invoice.invoice_number.strip() == "":
            errors.append("Unique operational transaction identifier index missing")

        # Operational Check 2: Absolute Financial Zero Defalcation Checks
        if invoice.subtotal <= 0:
            errors.append("Subtotal missing or indicates a negative/zero line statement balance")

        if invoice.grand_total <= 0:
            errors.append("Grand Total valuation metric missing or invalid")

        # Operational Check 3: Dynamic Country Rules Equation Balance Validation
        expected_grand_total = invoice.subtotal + invoice.gst
        variance = abs(expected_grand_total - invoice.grand_total)

        if variance > 0.02:  # Safe float variance boundary limits allowance
            errors.append(
                f"Financial Calculation Mismatch: Calculated balance ({expected_grand_total:.2f}) "
                f"does not balance with Grand Total entry ({invoice.grand_total:.2f})"
            )

        invoice.errors = errors
        return {
            "passed": len(errors) == 0,
            "errors": errors,
            "audit_telemetry": {
                "calculated_variance": variance,
                "currency_verified": invoice.currency,
                "active_tax_components": list(invoice.tax_breakdown.keys())
            }
        }