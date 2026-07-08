"""
===========================================================
Project Nexus Sentinel — Document Parser
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
        raw_lines = [self.utils.clean_line(l) for l in text.split("\n") if not self.utils.is_blank(l)]
        if not raw_lines:
            return []

        # Pass 1: Top-Down Header Scan
        for i, line in enumerate(raw_lines[:15]):
            line_lower = line.lower()
            
            if any(k in line_lower for k in FIELD_ALIASES["invoice_date"]):
                dt = self.utils.extract_date(line)
                if not dt and i + 1 < len(raw_lines):
                    dt = self.utils.extract_date(raw_lines[i + 1])
                if dt:
                    tokens.append(DocumentToken("invoice_date", dt, line, i, 1.0))

            if any(k in line_lower for k in FIELD_ALIASES["invoice_number"]):
                inv = self.utils.extract_invoice_number(line)
                if not inv and i + 1 < len(raw_lines):
                    inv = self.utils.extract_invoice_number(raw_lines[i + 1])
                if inv:
                    tokens.append(DocumentToken("invoice_number", inv, line, i, 1.0))

            if len(line) >= 3 and not self.utils.is_numeric(line):
                tokens.append(DocumentToken("raw_text_block", line, line, i, 0.50))

        # Pass 2: Bottom-Up Totals Scan
        reverse_lines = raw_lines[::-1]
        for idx, line in enumerate(reverse_lines):
            line_lower = line.lower()

            # Ignore product tables to prevent "Subtotal" collisions
            if any(k in line_lower for k in ["hsn", "qty", "rate", "description", "unit price"]):
                continue

            search_window = " ".join(reverse_lines[max(0, idx - 1): min(len(reverse_lines), idx + 3)])

            if any(k in line_lower for k in FIELD_ALIASES["grand_total"]):
                amounts = self.utils.extract_valid_amounts(search_window)
                if amounts:
                    tokens.append(DocumentToken("grand_total", str(max(amounts)), line, 0, 1.0))

            if any(k in line_lower for k in FIELD_ALIASES["gst"]):
                amounts = self.utils.extract_valid_amounts(search_window)
                if amounts:
                    tokens.append(DocumentToken("gst", str(amounts[0]), line, 0, 1.0))

            if any(k in line_lower for k in FIELD_ALIASES["subtotal"]):
                amounts = self.utils.extract_valid_amounts(search_window)
                if amounts:
                    tokens.append(DocumentToken("subtotal", str(amounts[0]), line, 0, 1.0))

        return tokens