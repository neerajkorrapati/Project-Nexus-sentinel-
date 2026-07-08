"""
===========================================================
Project Nexus — Country Rules Configuration Registry

Defines global enterprise tax compliance rules and multi-tenant
regulatory properties without hardcoding engine criteria.
===========================================================
"""

COUNTRY_TAX_REGISTRY = {
    "IN": {
        "country_name": "India",
        "primary_tax_name": "GST",
        "sub_tax_components": ["CGST", "SGST", "IGST"],
        "default_currency": "INR",
        "requires_gstin": True
    },
    "DE": {
        "country_name": "Germany",
        "primary_tax_name": "VAT",
        "sub_tax_components": ["MwSt"],
        "default_currency": "EUR",
        "requires_gstin": False
    },
    "US": {
        "country_name": "United States",
        "primary_tax_name": "Sales Tax",
        "sub_tax_components": ["State Tax", "County Tax", "City Tax"],
        "default_currency": "USD",
        "requires_gstin": False
    },
    "AE": {
        "country_name": "United Arab Emirates",
        "primary_tax_name": "VAT",
        "sub_tax_components": ["VAT Summary"],
        "default_currency": "AED",
        "requires_gstin": False
    },
    "SG": {
        "country_name": "Singapore",
        "primary_tax_name": "GST",
        "sub_tax_components": ["GST Summary"],
        "default_currency": "SGD",
        "requires_gstin": False
    }
}