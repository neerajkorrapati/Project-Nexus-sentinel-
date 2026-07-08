"""
===========================================================
Project Nexus — Reusable Platform Tax Engine

Executes country-specific tax calculations and compliance verification
checks dynamically across invoices or billing timesheet systems.
===========================================================
"""

import re
from typing import List, Dict
from models.document_token import DocumentToken
from rules.country_rules import COUNTRY_TAX_REGISTRY


class TaxEngine:

    def calculate_tax_breakdown(self, tokens: List[DocumentToken], country_code: str = "IN") -> Dict[str, float]:
        """
        Calculates country-specific tax distributions dynamically using the country configuration rules.
        """
        breakdown = {}
        config = COUNTRY_TAX_REGISTRY.get(country_code, COUNTRY_TAX_REGISTRY["IN"])
        target_components = config["sub_tax_components"]

        # Step through every active token to pull tax items matching regional categories
        for token in tokens:
            if token.label == "gst" or token.label == "amount":
                token_text_lower = token.raw_text.lower()
                
                for component in target_components:
                    # Enforce strict boundary pattern matching to prevent substring collision vulnerabilities
                    if re.search(rf"\b{re.escape(component.lower())}\b", token_text_lower):
                        matches = re.findall(r"\d+(?:,\d{3})*(?:\.\d{2})?", token.value)
                        if matches:
                            try:
                                val = float(matches[-1].replace(",", ""))
                                if val > 0 and component not in breakdown:
                                    breakdown[component] = val
                            except ValueError:
                                continue
        return breakdown

    def aggregate_total_tax(self, breakdown: Dict[str, float], extracted_gst: float) -> float:
        """
        Aggregates calculated sub-tax categories, falling back to the top-level metric if needed.
        """
        if not breakdown:
            return extracted_gst
            
        summed_components = sum(breakdown.values())
        # Use the maximum value between explicit extractions and combined elements for structural resilience
        return max(summed_components, extracted_gst)