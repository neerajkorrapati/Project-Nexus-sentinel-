"""
===========================================================
Invoice Agent V4

Extractor Utilities

Reusable helper functions shared by every extractor.

Author: Project Nexus
===========================================================
"""

import re

from rules.field_aliases import FIELD_ALIASES


class ExtractorUtils:

    # ---------------------------------------------------
    # Normalize a line
    # ---------------------------------------------------

    @staticmethod
    def clean(line: str) -> str:

        if line is None:
            return ""

        return line.strip().lower()

    # ---------------------------------------------------
    # Does this line contain any alias?
    # ---------------------------------------------------

    @staticmethod
    def contains_alias(line: str, aliases: list) -> bool:

        line = ExtractorUtils.clean(line)

        for alias in aliases:

            if alias.lower() in line:
                return True

        return False

    # ---------------------------------------------------
    # Get aliases for a field
    # ---------------------------------------------------

    @staticmethod
    def aliases(field_name: str):

        return FIELD_ALIASES.get(field_name, [])

    # ---------------------------------------------------
    # Extract value after ':'
    # ---------------------------------------------------

    @staticmethod
    def value_after_colon(line: str):

        parts = line.split(":", 1)

        if len(parts) == 2:

            return parts[1].strip()

        return ""

    # ---------------------------------------------------
    # Extract first decimal/integer number
    # ---------------------------------------------------

    @staticmethod
    def extract_number(line: str):

        matches = re.findall(r"\d+\.\d+|\d+", line)

        if not matches:
            return None

        try:
            return float(matches[-1])
        except Exception:
            return None

    # ---------------------------------------------------
    # Extract first date
    # ---------------------------------------------------

    @staticmethod
    def extract_date(line: str):

        patterns = [

            r"\d{2}/\d{2}/\d{4}",
            r"\d{2}-\d{2}-\d{4}",
            r"\d{4}-\d{2}-\d{2}"

        ]

        for pattern in patterns:

            result = re.search(pattern, line)

            if result:

                return result.group()

        return ""

    # ---------------------------------------------------
    # Remove currency symbols
    # ---------------------------------------------------

    @staticmethod
    def remove_currency(line: str):

        line = line.replace("₹", "")

        line = line.replace("$", "")

        line = line.replace("Rs.", "")

        line = line.replace("Rs", "")

        line = line.replace("INR", "")

        return line.strip()

    # ---------------------------------------------------
    # Is this line empty?
    # ---------------------------------------------------

    @staticmethod
    def is_blank(line: str):

        return len(line.strip()) == 0

    # ---------------------------------------------------
    # Find line containing a field alias
    # ---------------------------------------------------

    @staticmethod
    def find_matching_line(lines, field):

        aliases = ExtractorUtils.aliases(field)

        for line in lines:

            if ExtractorUtils.contains_alias(line, aliases):

                return line

        return ""

    # ---------------------------------------------------
    # Get next non-empty line
    # ---------------------------------------------------

    @staticmethod
    def next_non_empty(lines, index):

        for i in range(index + 1, len(lines)):

            if not ExtractorUtils.is_blank(lines[i]):

                return lines[i]

        return ""

    # ---------------------------------------------------
    # Print debug
    # ---------------------------------------------------

    @staticmethod
    def debug(title, value):

        print(f"[DEBUG] {title}: {value}")