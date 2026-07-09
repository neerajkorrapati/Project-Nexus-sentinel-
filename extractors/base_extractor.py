"""
===========================================================
Project Nexus - Base Extractor Interface
===========================================================
"""

from parser.parser_utils import ParserUtils


class BaseExtractor:

    def __init__(self):
        self.utils = ParserUtils()

    def debug(self, msg: str, value=None):
        if value is not None:
            print(f"[{self.__class__.__name__}] {msg}: {value}")
        else:
            print(f"[{self.__class__.__name__}] {msg}")

    def tokens_by_label(self, tokens: list, label: str) -> list:
        return [token for token in tokens if token.label == label]

    def alias_tokens(self, tokens: list, field_name: str) -> list:
        return [
            token for token in tokens
            if token.label == "field_alias" and token.value == field_name
        ]

    def line_tokens(self, tokens: list) -> list:
        return self.tokens_by_label(tokens, "line")

    def line_text(self, tokens: list, line_number: int) -> str:
        for token in tokens:
            if token.label == "line" and token.line_number == line_number:
                return token.value
        return ""

    def tokens_on_line(self, tokens: list, label: str, line_number: int) -> list:
        return [
            token for token in tokens
            if token.label == label and token.line_number == line_number
        ]

    def tokens_near_line(self, tokens: list, label: str, line_number: int, distance: int = 1) -> list:
        return [
            token for token in tokens
            if token.label == label and abs(token.line_number - line_number) <= distance
        ]

    def numeric_values(self, tokens: list) -> list:
        values = []
        for token in tokens:
            try:
                values.append(float(token.value))
            except (TypeError, ValueError):
                continue
        return values

    def amounts_for_alias(self, tokens: list, field_name: str, max_distance: int = 1) -> list:
        amounts = []
        for alias in self.alias_tokens(tokens, field_name):
            same_line = self.tokens_on_line(tokens, "amount", alias.line_number)
            nearby = same_line or self.tokens_near_line(tokens, "amount", alias.line_number, max_distance)
            for token in nearby:
                if token not in amounts:
                    amounts.append(token)
        return amounts

    def extract(self, tokens: list):
        raise NotImplementedError("Subclasses must implement extract()")
