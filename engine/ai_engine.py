"""
===========================================================
Project Nexus Sentinel — AI Rectification Engine
===========================================================
"""

import os
import json
import re
import google.generativeai as genai


class AIEngine:

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            print("[AIEngine Warning] GEMINI_API_KEY missing from environment variables!")
            
        self.model = genai.GenerativeModel('gemini-3.5-flash')

    def rectify_extraction(self, raw_text: str, deterministic_data: dict) -> dict:
        if not self.api_key:
            deterministic_data["vendor"] = "CRITICAL_ERROR: API KEY NOT FOUND"
            return deterministic_data

        # Token Compression: Remove empty lines to minimize API token cost
        compressed_ocr = "\n".join([line.strip() for line in raw_text.split("\n") if line.strip()])

        prompt = f"""
        You are an enterprise financial auditor. Extract the exact accounting details from this invoice.
        Ensure Subtotal + GST = Grand Total. If subtotal is missing, calculate it as Grand Total - GST.
        
        Target JSON Keys: "vendor", "invoice_number", "invoice_date", "subtotal", "gst", "grand_total".
        
        Raw Invoice Text:
        {compressed_ocr}
        """

        try:
            # Forcing raw JSON output at the model config level
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.0
                )
            )

            # Defensive parsing against Markdown code blocks
            raw_response = response.text.strip()
            clean_json = re.sub(r"^```(?:json)?", "", raw_response, flags=re.MULTILINE)
            clean_json = re.sub(r"```$", "", clean_json, flags=re.MULTILINE).strip()

            data = json.loads(clean_json)

            return {
                "vendor": str(data.get("vendor", deterministic_data.get("vendor", "UNKNOWN_VENDOR"))),
                "invoice_number": str(data.get("invoice_number", deterministic_data.get("invoice_number", "UNKNOWN"))),
                "invoice_date": str(data.get("invoice_date", deterministic_data.get("invoice_date", "UNKNOWN"))),
                "subtotal": float(data.get("subtotal", 0.0) or 0.0),
                "gst": float(data.get("gst", 0.0) or 0.0),
                "grand_total": float(data.get("grand_total", 0.0) or 0.0)
            }

        except Exception as e:
            print(f"[AIEngine Error] Gemini Escalation Failed: {e}")
            # Surface the actual Python error in the JSON response so you can see it in Swagger!
            deterministic_data["vendor"] = f"AI_ERROR: {str(e)}"
            return deterministic_data