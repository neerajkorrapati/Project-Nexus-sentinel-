"""
===========================================================
Project Nexus Sentinel - Document Parser

Produces neutral document tokens. Business decisions belong to extractors.
===========================================================
"""

from models.document_token import DocumentToken
from parser.parser_utils import ParserUtils
from rules.field_aliases import FIELD_ALIASES


class DocumentParser:

    def __init__(self):
        self.utils = ParserUtils()

    def parse(self, text: str):
        if not text:
            return []

        tokens = []
        pages = self.utils.split_pages(text)
        if not pages:
            return []

        global_line_number = 0

        for page_index, lines in enumerate(pages, start=1):
            for page_line_number, line in enumerate(lines, start=1):
                global_line_number += 1
                tokens.append(
                    DocumentToken(
                        label="line",
                        value=line,
                        raw_text=line,
                        line_number=global_line_number,
                        confidence=1.0,
                        page_number=page_index,
                        metadata={"page_line_number": page_line_number},
                    )
                )

                for field_name in self.utils.matching_fields(line, FIELD_ALIASES):
                    tokens.append(
                        DocumentToken(
                            label="field_alias",
                            value=field_name,
                            raw_text=line,
                            line_number=global_line_number,
                            confidence=0.92,
                            page_number=page_index,
                            field_name=field_name,
                        )
                    )

                for amount in self.utils.extract_amounts(line):
                    tokens.append(
                        DocumentToken(
                            label="amount",
                            value=amount,
                            raw_text=line,
                            line_number=global_line_number,
                            confidence=0.90,
                            page_number=page_index,
                        )
                    )

                for date_value in self.utils.extract_dates(line):
                    tokens.append(
                        DocumentToken(
                            label="date",
                            value=date_value,
                            raw_text=line,
                            line_number=global_line_number,
                            confidence=0.90,
                            page_number=page_index,
                        )
                    )

                for identifier in self.utils.extract_identifier_candidates(line):
                    tokens.append(
                        DocumentToken(
                            label="identifier",
                            value=identifier,
                            raw_text=line,
                            line_number=global_line_number,
                            confidence=0.78,
                            page_number=page_index,
                        )
                    )

                for currency in self.utils.detect_currency_codes(line):
                    tokens.append(
                        DocumentToken(
                            label="currency",
                            value=currency,
                            raw_text=line,
                            line_number=global_line_number,
                            confidence=0.88,
                            page_number=page_index,
                        )
                    )

        return tokens

    def print_tokens(self, tokens):
        for token in tokens:
            print(token)
