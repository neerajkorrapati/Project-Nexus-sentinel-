"""
===========================================================
Project Nexus — Enterprise Document Parser

Generates a multi-candidate token stream using a Strict Line-Bound
Slicing Engine to defeat layout fragmentation and spacing errors.
===========================================================
"""

import re
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
        
        priority_queue = []
        for label, aliases in FIELD_ALIASES.items():
            for alias in aliases:
                priority_queue.append((label, alias.lower()))
        priority_queue.sort(key=lambda x: len(x[1]), reverse=True)

        # Ignore metadata searches inside complex product tables to prevent header hijacking
        table_headers = ["qty", "rate", "hsn", "description", "product", "discount", "vehicle", "s. no."]

        for i, line in enumerate(raw_lines):
            line_lower = line.lower()
            
            if any(th in line_lower for th in table_headers):
                continue

            matched_labels = set()

            for label, alias in priority_queue:
                if label in matched_labels:
                    continue

                # Strict boundary check (letters/numbers cannot surround the alias - protects 'gst' from 'gstin')
                pattern = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
                match = re.search(pattern, line_lower)
                
                if match:
                    final_value = None
                    
                    # Slice text exactly AFTER the keyword to prevent grabbing numbers that came before it
                    post_text = line[match.end():]

                    if label in ["subtotal", "gst", "grand_total"]:
                        # 1. Check the exact same line downstream
                        amounts = self.utils.extract_valid_amounts(post_text)
                        
                        # 2. Fallback: Check the entire line
                        if not amounts:
                            amounts = self.utils.extract_valid_amounts(line)
                            
                        # 3. Fallback: Check the next line (max 1 line lookahead to prevent bleed)
                        if not amounts and i + 1 < len(raw_lines):
                            amounts = self.utils.extract_valid_amounts(raw_lines[i+1])
                            
                        if amounts:
                            # Grab the FIRST valid amount in the downstream text sequence
                            final_value = amounts[0]
                            
                    elif label == "invoice_date":
                        final_value = self.utils.extract_date(post_text)
                        if not final_value:
                            final_value = self.utils.extract_date(line)
                        if not final_value and i + 1 < len(raw_lines):
                            final_value = self.utils.extract_date(raw_lines[i+1])
                            
                    elif label == "invoice_number":
                        final_value = self.utils.extract_invoice_number(post_text)
                        if not final_value:
                            final_value = self.utils.extract_invoice_number(line)
                        if not final_value and i + 1 < len(raw_lines):
                            final_value = self.utils.extract_invoice_number(raw_lines[i+1])
                            
                    else:
                        final_value = line.replace(":", "").replace("|", "").strip()

                    if final_value:
                        tokens.append(DocumentToken(
                            label=label,
                            value=str(final_value),
                            raw_text=line,
                            line_number=i,
                            confidence=1.0
                        ))
                        matched_labels.add(label)

        # Pass 2: Contextual Line Tracking for Header Vendor Identification
        for i, line in enumerate(raw_lines):
            if len(line) >= 3 and not self.utils.is_numeric(line):
                tokens.append(DocumentToken(
                    label="raw_text_block",
                    value=line,
                    raw_text=line,
                    line_number=i,
                    confidence=0.50
                ))

        return tokens

    def print_tokens(self, tokens):
        print("\n========== DOCUMENT TOKENS ==========\n")
        for token in tokens:
            print(token)