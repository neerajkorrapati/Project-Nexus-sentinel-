"""
===========================================================
Project Nexus Sentinel - AI Rectification Engine
===========================================================
"""

import json
import os
import re
from typing import Any, Optional


class AIEngine:

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        self.client: Optional[Any] = None

        if not self.api_key:
            print("[AIEngine Warning] GEMINI_API_KEY missing from environment variables!")

    def _get_client(self):
        if self.client is not None:
            return self.client

        if not self.api_key:
            return None

        try:
            from google import genai
        except ImportError:
            print("[AIEngine Warning] google-genai is not installed. AI fallback disabled.")
            return None

        self.client = genai.Client(api_key=self.api_key)
        return self.client

    def rectify_extraction(self, raw_text: str, deterministic_data: dict) -> dict:
        client = self._get_client()
        if client is None:
            deterministic_data["ai_fallback_error"] = "AI fallback unavailable: missing API key or google-genai package."
            return deterministic_data

        compressed_ocr = "\n".join(line.strip() for line in raw_text.split("\n") if line.strip())

        prompt = f"""
        You are an enterprise financial auditor. Extract the exact accounting details from this invoice.
        Ensure Subtotal + GST = Grand Total. If subtotal is missing, calculate it as Grand Total - GST.

        Return only JSON with these keys:
        "vendor", "invoice_number", "invoice_date", "subtotal", "gst", "grand_total".

        Raw Invoice Text:
        {compressed_ocr}
        """

        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0.0,
                },
            )

            raw_response = (response.text or "").strip()
            clean_json = re.sub(r"^```(?:json)?", "", raw_response, flags=re.MULTILINE)
            clean_json = re.sub(r"```$", "", clean_json, flags=re.MULTILINE).strip()

            data = json.loads(clean_json)

            return {
                "vendor": str(data.get("vendor", deterministic_data.get("vendor", "UNKNOWN_VENDOR"))),
                "invoice_number": str(data.get("invoice_number", deterministic_data.get("invoice_number", "UNKNOWN"))),
                "invoice_date": str(data.get("invoice_date", deterministic_data.get("invoice_date", "UNKNOWN"))),
                "currency": str(data.get("currency", deterministic_data.get("currency", "INR"))),
                "subtotal": float(data.get("subtotal", deterministic_data.get("subtotal", 0.0)) or 0.0),
                "gst": float(data.get("gst", deterministic_data.get("gst", 0.0)) or 0.0),
                "grand_total": float(data.get("grand_total", deterministic_data.get("grand_total", 0.0)) or 0.0),
            }

        except Exception as exc:
            print(f"[AIEngine Error] Gemini escalation failed: {exc}")
            deterministic_data["ai_fallback_error"] = str(exc)
            return deterministic_data
