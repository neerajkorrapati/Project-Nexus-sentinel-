"""
===========================================================
Project Nexus — Parser Utilities

Production-grade extraction helpers built for high-accuracy 
financial parsing. Immune to dates, percentages, and serials.
===========================================================
"""

import re


class ParserUtils:

    @staticmethod
    def clean_line(line: str) -> str:
        if line is None:
            return ""
        line = line.replace("\t", " ")
        line = re.sub(r"\s+", " ", line)
        return line.strip()

    @staticmethod
    def is_blank(line: str) -> bool:
        return len(ParserUtils.clean_line(line)) == 0

    @staticmethod
    def extract_valid_amounts(text_block: str) -> list:
        """
        Extracts all valid financial amounts in a text window,
        actively filtering out percentages, dates, and layout serials.
        """
        if not text_block:
            return []
            
        # Actively destroy percentages so they are never parsed as financial amounts
        clean = re.sub(r"\b\d+(?:\.\d+)?\s*%", " ", text_block)
        clean = re.sub(r"\(\s*\d+(?:\.\d+)?\s*%\s*\)", " ", clean)
        
        # Clean currency symbols and structural table noise
        clean = clean.replace("₹", " ").replace("$", " ").replace("Rs.", " ").replace("rs.", " ")
        clean = clean.replace("|", " ").replace(":", " ").replace(",", "")
        
        # Locate all structural number blocks
        matches = re.findall(r"\b\d+(?:\.\d{1,2})?\b", clean)
        
        valid_amounts = []
        for m in matches:
            try:
                val = float(m)
                # Ignore standard calendar years (e.g., 2017, 2026)
                if 1900 <= val <= 2099 and "." not in m:
                    continue
                # Accept float decimals or values >= 10 (ignores 1, 2 table indexes)
                if "." in m or val >= 10.0:
                    valid_amounts.append(val)
            except ValueError:
                continue
                
        return valid_amounts

    @staticmethod
    def extract_date(text_block: str):
        patterns = [
            r"\b\d{2}/\d{2}/\d{4}\b",
            r"\b\d{2}-\d{2}-\d{4}\b",
            r"\b\d{4}/\d{2}/\d{2}\b",
            r"\b\d{4}-\d{2}-\d{2}\b"
        ]
        for pattern in patterns:
            match = re.search(pattern, text_block)
            if match:
                return match.group()
        return None

    @staticmethod
    def extract_invoice_number(text_block: str):
        patterns = [
            r"\b[A-Za-z0-9]+[-/]\d+[-/][A-Za-z0-9]+\b",
            r"\b[A-Za-z0-9]+[-/]\d+[-/]\d+\b",
            r"\b[A-Za-z0-9]+[-/]\d+\b",
            r"\b\d{4}-\d{2}/\d+\b",
            r"\b[A-Za-z0-9]{3,15}\b"
        ]
        for pattern in patterns:
            match = re.search(pattern, text_block)
            if match:
                return match.group()
        return None

    @staticmethod
    def is_numeric(value: str) -> bool:
        try:
            float(value.replace(",", "").replace(" ", ""))
            return True
        except ValueError:
            return False