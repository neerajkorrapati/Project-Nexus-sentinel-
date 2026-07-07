"""
===========================================================

Invoice Agent V3.5

Parser Utilities

Reusable helper functions for
DocumentParser.

===========================================================
"""

import re


class ParserUtils:

    @staticmethod
    def clean_line(line: str):

        if line is None:
            return ""

        line = line.replace("\t", " ")

        line = re.sub(r"\s+", " ", line)

        return line.strip()

    # --------------------------------------------------
    # Is this line empty?
    # --------------------------------------------------

    @staticmethod
    def is_blank(line):

        return len(ParserUtils.clean_line(line)) == 0

    # --------------------------------------------------
    # Detect Key : Value
    # --------------------------------------------------

    @staticmethod
    def split_key_value(line):

        line = ParserUtils.clean_line(line)

        if ":" not in line:

            return None

        key, value = line.split(":", 1)

        return key.strip(), value.strip()

    # --------------------------------------------------
    # Detect Amount
    # --------------------------------------------------

    @staticmethod
    def extract_amount(line):

        pattern = r"\d+(?:,\d{3})*(?:\.\d{2})?"

        matches = re.findall(pattern, line)

        if not matches:

            return None

        amount = matches[-1]

        amount = amount.replace(",", "")

        return amount

    # --------------------------------------------------
    # Detect Date
    # --------------------------------------------------

    @staticmethod
    def extract_date(line):

        patterns = [

            r"\d{2}/\d{2}/\d{4}",

            r"\d{2}-\d{2}-\d{4}",

            r"\d{4}/\d{2}/\d{2}",

            r"\d{4}-\d{2}-\d{2}"

        ]

        for pattern in patterns:

            match = re.search(pattern, line)

            if match:

                return match.group()

        return None

    # --------------------------------------------------
    # Invoice Number Detection
    # --------------------------------------------------

    @staticmethod
    def extract_invoice_number(line):

        patterns = [

            r"[A-Za-z]+[-/]\d+",

            r"\d{4}-\d{2}/\d+",

            r"[A-Za-z0-9/-]{6,}"

        ]

        for pattern in patterns:

            match = re.search(pattern, line)

            if match:

                return match.group()

        return None

    # --------------------------------------------------
    # Normalize Key
    # --------------------------------------------------

    @staticmethod
    def normalize_key(key):

        key = key.lower()

        key = key.replace("_", " ")

        key = re.sub(r"\s+", " ", key)

        return key.strip()

    # --------------------------------------------------
    # Is Numeric?
    # --------------------------------------------------

    @staticmethod
    def is_numeric(value):

        try:

            float(value.replace(",", ""))

            return True

        except:

            return False

    # --------------------------------------------------
    # Print Debug
    # --------------------------------------------------

    @staticmethod
    def debug(title, value):

        print(f"[Parser] {title}: {value}")