"""
===========================================================
Project Nexus — Currency Engine
===========================================================
"""


class CurrencyEngine:

    @staticmethod
    def normalize_amount(value_str: str) -> float:
        if not value_str:
            return 0.0
        try:
            clean = str(value_str).replace("₹", "").replace("$", "").replace("Rs.", "").replace(",", "").strip()
            return float(clean)
        except ValueError:
            return 0.0