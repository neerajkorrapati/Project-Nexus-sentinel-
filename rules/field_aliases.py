"""
===========================================================
Project Nexus - Field Alias Dictionary

Aliases describe document language only. They do not perform extraction.
Extractors decide how to interpret nearby tokens.
===========================================================
"""

FIELD_ALIASES = {
    "vendor": [
        "supplier",
        "seller",
        "vendor",
        "from",
    ],
    "invoice_number": [
        "invoice no",
        "invoice number",
        "invoice #",
        "inv no",
        "inv number",
        "bill no",
        "document no",
        "tax invoice no",
    ],
    "invoice_date": [
        "invoice date",
        "date of invoice",
        "date of supply",
        "bill date",
        "dated",
        "date",
    ],
    "subtotal": [
        "total amount before tax",
        "taxable value",
        "subtotal",
        "sub total",
        "net amount",
        "assessable value",
        "taxable amount",
        "amount before tax",
    ],
    "gst": [
        "add: c gst + s gst",
        "c gst + s gst",
        "cgst + sgst",
        "s gst + c gst",
        "total tax amount",
        "gst amount",
        "total tax",
        "cgst",
        "sgst",
        "igst",
        "gst",
    ],
    "grand_total": [
        "total amount after tax",
        "grand total",
        "total invoice amount",
        "invoice total",
        "net payable",
        "amount payable",
        "total payable",
        "balance due",
        "amount due",
        "total",
    ],
    "currency": [
        "currency",
        "inr",
        "usd",
        "eur",
        "aed",
        "sgd",
        "rs.",
        "rs",
    ],
}
