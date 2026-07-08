"""
===========================================================
Project Nexus — Field Aliases Dictionary

Maps standard internal schema keys to common OCR text variations
found across Indian and international invoice formats.
===========================================================
"""

FIELD_ALIASES = {
    "subtotal": [
        "total amount before tax",
        "taxable value",
        "subtotal",
        "sub total",
        "net amount",
        "assessable value",
        "taxable amount"
    ],
    "gst": [
        "add: c gst + s gst",
        "c gst + s gst",
        "cgst + sgst",
        "s gst + c gst",
        "total tax amount",
        "gst amount",
        "total tax",
        "igst",
        "gst"
    ],
    "grand_total": [
        "total amount after tax",
        "grand total",
        "total invoice amount",
        "invoice total",
        "net payable",
        "amount payable",
        "total payable",
        "total"
    ],
    "invoice_number": [
        "invoice no",
        "invoice number",
        "inv no",
        "bill no",
        "document no"
    ],
    "invoice_date": [
        "invoice date",
        "date of supply",
        "dated",
        "bill date",
        "date"
    ]
}