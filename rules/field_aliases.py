"""
===========================================================
Invoice Agent V3
Field Alias Dictionary

This file contains every keyword that can represent
a particular invoice field.

Instead of hardcoding:

    if line.startswith("Invoice Number")

the extraction engine asks this file for all possible
aliases.

Easy to maintain.
Easy to extend.
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
        "company",
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
        "date",
        "billing date",
        "issue date"

    ],

    # --------------------------------------------------
    # Due Date
    # --------------------------------------------------

    "due_date": [

        "due date",
        "payment due",
        "payment date"

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
        "amount before tax"

    ],

    # --------------------------------------------------
    # GST
    # --------------------------------------------------

    "gst": [

        "gst",
        "cgst",
        "sgst",
        "igst",
        "tax amount",
        "tax"

    ],

    # --------------------------------------------------
    # Grand Total
    # --------------------------------------------------

    "grand_total": [

        "grand total",
        "invoice total",
        "total amount",
        "amount payable",
        "net amount",
        "net payable",
        "invoice value"

    ]

}