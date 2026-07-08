"""
===========================================================
Project Nexus — Reusable Platform Currency Engine

Stateless service providing currency symbol normalization,
formatting compliance controls, and evaluation routines.
===========================================================
"""

import re


class CurrencyEngine:

    def __init__(self):
        # Maps raw visual symbols back to standardized ISO codes
        self.symbol_map = {
            "₹": "INR",
            "rs": "INR",
            "$": "USD",
            "€": "EUR",
            "aed": "AED",
            "sgd": "SGD",
            "£": "GBP"
        }

    def detect_currency(self, text_stream: str, fallback_country: str = "IN") -> str:
        """
        Scans document text strings to identify the correct ISO currency token.
        """
        if not text_stream:
            return "INR"

        text_lower = text_stream.lower()
        for symbol, iso_code in self.symbol_map.items():
            if symbol in text_lower:
                return iso_code

        # Revert back to country defaults if direct visual identifiers are absent
        from rules.country_rules import COUNTRY_TAX_REGISTRY
        return COUNTRY_TAX_REGISTRY.get(fallback_country, {}).get("default_currency", "INR")

    def normalize_amount(self, raw_value: str) -> float:
        """
        Scrubs financial numerical entries cleanly across diverse cultural format boundaries.
        """
        if not raw_value:
            return 0.0
            
        # Strip structural noise, currencies, and spaces
        clean = re.sub(r"[^\d\.\-]", "", raw_value.replace(",", ""))
        try:
            return float(clean) if clean else 0.0
        except ValueError:
            return 0.0