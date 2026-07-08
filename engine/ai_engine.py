"""
===========================================================
Project Nexus — AI Rectification Engine

Acts as a fallback layer. When the deterministic parser fails,
this engine injects the raw text and the failing data into Gemini
to logically deduce and correct the missing accounting fields.
===========================================================
"""

import os
import json
import google.generativeai as genai


class AIEngine:
    def __init__(self):
        # Ensure your environment variable GEMINI_API_KEY is set
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            
        # gemini-1.5-flash is used for maximum speed and cost efficiency
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def rectify_extraction(self, raw_text: str, deterministic_data: dict) -> dict:
        """
        Sends the compressed OCR text and the broken deterministic payload to the AI
        and forces a strictly typed JSON response containing the corrected values.
        """
        prompt = f"""
        You are an expert enterprise financial data extraction agent. 
        A deterministic regex parser attempted to extract invoice data from the following OCR text, 
        but it failed mathematical validation (e.g., Subtotal + GST != Grand Total).
        
        Current Failing Deterministic Data:
        {json.dumps(deterministic_data, indent=2)}

        Raw Document OCR Text:
        {raw_text}

        Task: 
        1. Review the OCR text.
        2. Find the true mathematical totals.
        3. Rectify the errors in the deterministic data.
        
        Rules:
        - Return ONLY a raw JSON object.
        - The JSON must contain exactly these keys: "vendor" (str), "invoice_number" (str), "invoice_date" (str), "subtotal" (float), "gst" (float), "grand_total" (float).
        - Ensure Subtotal + GST = Grand Total.
        - Do not include markdown blocks, explanations, or formatting.
        """
        
        try:
            # Enforce strict JSON output to guarantee pipeline stability
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.0  # Zero creativity; strict factual extraction
                )
            )
            # Parse the guaranteed JSON response directly into a Python dictionary
            return json.loads(response.text)
            
        except Exception as e:
            print(f"[AI Escalation Failed] {e}")
            # Failsafe: Return the original deterministic data if the API is unreachable
            return deterministic_data