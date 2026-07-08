"""
===========================================================
Project Nexus Sentinel — Parser Utilities
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
        if not text_block:
            return []

        # Destroy percentages so tax rates are never parsed as monetary amounts
        clean = re.sub(r"\(?\[?\b\d+(?:\.\d+)?\s*%\)?\]?", " ", text_block)
        
        # Destroy currency symbols and table row barriers
        clean = clean.replace("₹", " ").replace("$", " ").replace("Rs.", " ").replace("rs.", " ")
        clean = clean.replace("|", " ").replace(":", " ")

        matches = re.findall(r"\b\d+(?:,\d{3})*(?:\.\d{2})?\b", clean)
        amounts = []

        for m in matches:
            val_str = m.replace(",", "")
            try:
                val = float(val_str)
                # Ignore calendar years unless formatted explicitly as money
                if 1900 <= val <= 2099 and "." not in val_str:
                    continue
                # Ignore table serial lines (1, 2, 3)
                if val >= 10.0 or "." in val_str:
                    amounts.append(val)
            except ValueError:
                continue

        return amounts

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
            r"\b[A-Za-z0-9]{4,15}\b"
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