"""
===========================================================
Project Nexus - Currency Engine
===========================================================
"""


class CurrencyEngine:

    @staticmethod
    def normalize_amount(value_str: str) -> float:
        if not value_str:
            return 0.0
        try:
            clean = str(value_str)
            for symbol in ["₹", "â‚¹", "$", "Rs.", "Rs", "INR"]:
                clean = clean.replace(symbol, "")
            clean = clean.replace(",", "").strip()
            return float(clean)
        except ValueError:
            return 0.0

    @staticmethod
    def detect_currency(text: str, fallback_country: str = "IN") -> str:
        if not text:
            return "INR" if fallback_country == "IN" else "USD"

        lowered = text.lower()
        if "₹" in text or "â‚¹" in text or "inr" in lowered or "rs." in lowered:
            return "INR"
        if "$" in text or "usd" in lowered:
            return "USD"
        if "€" in text or "eur" in lowered:
            return "EUR"
        if "aed" in lowered:
            return "AED"
        if "sgd" in lowered:
            return "SGD"

        return "INR" if fallback_country == "IN" else "USD"
