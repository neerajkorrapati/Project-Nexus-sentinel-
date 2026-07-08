"""
===========================================================
Invoice Agent V4
Field Alias Dictionary

Maintains all recognized key phrases for structural field mapping.
===========================================================
"""

FIELD_ALIASES = {
    # --------------------------------------------------
    # Vendor
    # --------------------------------------------------
    "vendor": [
        "vendor",
        "supplier",
        "seller",
        "company name",
        "sold by",
        "bill from",
        "invoice from"
    ],

    # --------------------------------------------------
    # Invoice Number
    # --------------------------------------------------
    "invoice_number": [
        "invoice number",
        "invoice no",
        "invoice #",
        "tax invoice no",
        "document no",
        "bill no",
        "bill number",
        "reference number"
    ],

    # --------------------------------------------------
    # Invoice Date
    # --------------------------------------------------
    "invoice_date": [
        "invoice date",
        "bill date",
        "date of issue",
        "issue date",
        "date"
    ],

    # --------------------------------------------------
    # Subtotal
    # --------------------------------------------------
    "subtotal": [
        "subtotal",
        "sub total",
        "taxable amount",
        "taxable value",
        "basic amount",
        "amount before tax",
        "total amount before tax"
    ],

    # --------------------------------------------------
    # GST
    # --------------------------------------------------
    "gst": [
        "c gst + s gst",
        "s gst + c gst",
        "add c gst",
        "add s gst",
        "tax amount",
        "cgst",
        "sgst",
        "igst",
        "gst"
    ],

    # --------------------------------------------------
    # Grand Total
    # --------------------------------------------------
    "grand_total": [
        "total amount after tax",
        "grand total",
        "invoice total",
        "amount payable",
        "net amount",
        "net payable",
        "invoice value"
    ]
}