"""
===========================================================
Project Nexus — Document Token Model
===========================================================
"""

from dataclasses import dataclass


@dataclass
class DocumentToken:
    label: str
    value: str
    raw_text: str
    line_number: int
    confidence: float = 1.0

    def __str__(self):
        return f"Token({self.label} -> '{self.value}' | Conf: {self.confidence})"