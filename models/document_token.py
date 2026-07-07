"""
===========================================================

Invoice Agent V4

Document Token

A normalized representation of one piece of information
found inside a document.

Future ready for LayoutLM / Donut.

===========================================================
"""

from dataclasses import dataclass, field
from typing import Tuple, Optional


@dataclass
class DocumentToken:

    # ----------------------------------------
    # Semantic Information
    # ----------------------------------------

    label: str = ""

    value: str = ""

    # ----------------------------------------
    # Source Information
    # ----------------------------------------

    raw_text: str = ""

    source: str = "OCR"

    page: int = 1

    line_number: int = -1

    # ----------------------------------------
    # Layout Information
    # ----------------------------------------

    bbox: Optional[Tuple[int, int, int, int]] = None

    # ----------------------------------------
    # Confidence
    # ----------------------------------------

    confidence: float = 1.0

    # ----------------------------------------
    # Metadata
    # ----------------------------------------

    metadata: dict = field(default_factory=dict)

    def to_dict(self):

        return {

            "label": self.label,

            "value": self.value,

            "raw_text": self.raw_text,

            "source": self.source,

            "page": self.page,

            "line_number": self.line_number,

            "bbox": self.bbox,

            "confidence": self.confidence,

            "metadata": self.metadata

        }

    def __str__(self):

        return (

            f"[{self.label}] "

            f"{self.value} "

            f"(page={self.page}, "

            f"line={self.line_number}, "

            f"confidence={self.confidence:.2f})"

        )