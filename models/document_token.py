"""
===========================================================
Project Nexus - Document Token Model
===========================================================
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class DocumentToken:
    label: str
    value: str
    raw_text: str
    line_number: int
    confidence: float = 1.0
    page_number: int = 1
    field_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        page = f"p{self.page_number}:l{self.line_number}"
        field = f" | Field: {self.field_name}" if self.field_name else ""
        return f"Token({self.label} -> '{self.value}' | {page} | Conf: {self.confidence}{field})"
