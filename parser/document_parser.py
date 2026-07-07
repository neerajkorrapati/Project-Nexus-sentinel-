"""
===========================================================

Invoice Agent V4

Document Parser

Converts OCR text into structured DocumentTokens.

Author : Project Nexus

===========================================================
"""

from models.document_token import DocumentToken
from parser.parser_utils import ParserUtils
from rules.field_aliases import FIELD_ALIASES


class DocumentParser:

    def __init__(self):

        self.utils = ParserUtils()

    # ----------------------------------------------------
    # Main Entry
    # ----------------------------------------------------

    def parse(self, text):

        if text is None:
            return []

        tokens = []

        lines = text.split("\n")

        for line_number, line in enumerate(lines):

            line = self.utils.clean_line(line)

            if self.utils.is_blank(line):
                continue

            token = self.parse_line(line, line_number)

            if token:
                tokens.append(token)

        return tokens

    # ----------------------------------------------------
    # Parse Individual Line
    # ----------------------------------------------------

    def parse_line(self, line, line_number):

        key_value = self.utils.split_key_value(line)

        if key_value:

            key, value = key_value

            label = self.resolve_alias(key)

            return DocumentToken(

                label=label,

                value=value,

                line_number=line_number,

                confidence=1.0

            )

        # --------------------------------------------
        # Invoice Number
        # --------------------------------------------

        invoice = self.utils.extract_invoice_number(line)

        if invoice:

            return DocumentToken(

                label="invoice_number",

                value=invoice,

                line_number=line_number,

                confidence=0.90

            )

        # --------------------------------------------
        # Date
        # --------------------------------------------

        date = self.utils.extract_date(line)

        if date:

            return DocumentToken(

                label="invoice_date",

                value=date,

                line_number=line_number,

                confidence=0.90

            )

        # --------------------------------------------
        # Amount
        # --------------------------------------------

        amount = self.utils.extract_amount(line)

        if amount:

            return DocumentToken(

                label="amount",

                value=amount,

                line_number=line_number,

                confidence=0.80

            )

        return None

    # ----------------------------------------------------
    # Alias Resolution
    # ----------------------------------------------------

    def resolve_alias(self, key):

        key = self.utils.normalize_key(key)

        for field, aliases in FIELD_ALIASES.items():

            for alias in aliases:

                if alias.lower() == key:

                    return field

        return key

    # ----------------------------------------------------
    # Debug
    # ----------------------------------------------------

    def print_tokens(self, tokens):

        print("\n========== DOCUMENT TOKENS ==========\n")

        for token in tokens:

            print(token)