"""
===========================================================
Project Nexus Sentinel - Parser Utilities
===========================================================
"""

import re
from datetime import datetime
from typing import Dict, Iterable, List


class ParserUtils:

    CURRENCY_SYMBOLS = {
        "\u20b9": "INR",
        "Rs.": "INR",
        "Rs": "INR",
        "INR": "INR",
        "$": "USD",
        "USD": "USD",
        "EUR": "EUR",
        "AED": "AED",
        "SGD": "SGD",
    }

    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""

        replacements = {
            "\t": " ",
            "\r\n": "\n",
            "\r": "\n",
            "â‚¹": "\u20b9",
            "Ã¢â€šÂ¹": "\u20b9",
            "Invo1ce": "Invoice",
            "Inv0ice": "Invoice",
            "TotaI": "Total",
            "Sub Tota1": "Subtotal",
            "Arnount": "Amount",
            "arnount": "amount",
        }
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)

        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def clean_line(line: str) -> str:
        if line is None:
            return ""
        line = line.replace("\t", " ")
        line = re.sub(r"\s+", " ", line)
        return line.strip()

    @staticmethod
    def normalize_for_match(value: str) -> str:
        value = ParserUtils.clean_line(value).lower()
        value = value.replace("#", " number ")
        value = re.sub(r"[^a-z0-9%+./ -]", " ", value)
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    @staticmethod
    def is_blank(line: str) -> bool:
        return len(ParserUtils.clean_line(line)) == 0

    @staticmethod
    def split_pages(text: str) -> List[List[str]]:
        normalized = ParserUtils.normalize_text(text)
        if not normalized:
            return []

        pages = []
        for page_text in normalized.split("\f"):
            lines = [ParserUtils.clean_line(line) for line in page_text.split("\n")]
            pages.append([line for line in lines if line])
        return pages

    @staticmethod
    def contains_alias(line: str, alias: str) -> bool:
        clean_line = ParserUtils.normalize_for_match(line)
        clean_alias = ParserUtils.normalize_for_match(alias)
        if not clean_alias:
            return False
        return re.search(rf"(^|[^a-z0-9]){re.escape(clean_alias)}([^a-z0-9]|$)", clean_line) is not None

    @staticmethod
    def matching_fields(line: str, aliases: Dict[str, Iterable[str]]) -> List[str]:
        matches = []
        for field_name, field_aliases in aliases.items():
            if any(ParserUtils.contains_alias(line, alias) for alias in field_aliases):
                matches.append(field_name)
        return matches

    @staticmethod
    def extract_amounts(text_block: str) -> List[str]:
        if not text_block:
            return []

        clean = re.sub(r"\(?\[?\b\d+(?:\.\d+)?\s*%\)?\]?", " ", text_block)
        clean = clean.replace("|", " ").replace(":", " ")

        for symbol in ParserUtils.CURRENCY_SYMBOLS:
            clean = clean.replace(symbol, " ")

        matches = re.findall(r"(?<![\w/.-])\d+(?:,\d{2,3})*(?:\.\d{1,2})?(?![\w/.-])", clean)
        amounts = []
        for match in matches:
            val_str = match.replace(",", "")
            try:
                val = float(val_str)
                if 1900 <= val <= 2099 and "." not in val_str:
                    continue
                if val >= 10.0 or "." in val_str:
                    amounts.append(f"{val:.2f}")
            except ValueError:
                continue
        return amounts

    @staticmethod
    def extract_valid_amounts(text_block: str) -> list:
        return [float(value) for value in ParserUtils.extract_amounts(text_block)]

    @staticmethod
    def extract_dates(text_block: str) -> List[str]:
        patterns = [
            r"\b\d{1,2}/\d{1,2}/\d{4}\b",
            r"\b\d{1,2}-\d{1,2}-\d{4}\b",
            r"\b\d{4}/\d{1,2}/\d{1,2}\b",
            r"\b\d{4}-\d{1,2}-\d{1,2}\b",
            r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b",
            r"\b[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4}\b",
        ]
        found = []
        for pattern in patterns:
            for match in re.finditer(pattern, text_block):
                found.append(ParserUtils.normalize_date(match.group()))
        return found

    @staticmethod
    def extract_date(text_block: str):
        dates = ParserUtils.extract_dates(text_block)
        return dates[0] if dates else None

    @staticmethod
    def normalize_date(value: str) -> str:
        value = value.strip().replace(",", "")
        formats = [
            "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d",
            "%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d",
            "%d %b %Y", "%d %B %Y",
            "%b %d %Y", "%B %d %Y",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).date().isoformat()
            except ValueError:
                continue
        return value

    @staticmethod
    def extract_identifier_candidates(text_block: str) -> List[str]:
        patterns = [
            r"\b[A-Za-z]{1,6}[-/]\d{2,}[-/][A-Za-z0-9-]+\b",
            r"\b[A-Za-z]{1,6}[-/]\d{2,}\b",
            r"\b\d{4}-\d{2}/\d+\b",
            r"\b[A-Z0-9]{4,20}\b",
        ]
        candidates = []
        for pattern in patterns:
            for match in re.finditer(pattern, text_block):
                value = match.group().strip()
                if value not in candidates:
                    candidates.append(value)
        return candidates

    @staticmethod
    def extract_invoice_number(text_block: str):
        candidates = ParserUtils.extract_identifier_candidates(text_block)
        return candidates[0] if candidates else None

    @staticmethod
    def detect_currency_codes(text_block: str) -> List[str]:
        found = []
        for marker, code in ParserUtils.CURRENCY_SYMBOLS.items():
            if marker in text_block and code not in found:
                found.append(code)
        lowered = text_block.lower()
        for code in ["inr", "usd", "eur", "aed", "sgd"]:
            upper = code.upper()
            if re.search(rf"\b{code}\b", lowered) and upper not in found:
                found.append(upper)
        return found

    @staticmethod
    def is_numeric(value: str) -> bool:
        try:
            float(value.replace(",", "").replace(" ", ""))
            return True
        except ValueError:
            return False
