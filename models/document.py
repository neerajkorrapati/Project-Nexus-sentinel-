from dataclasses import dataclass
from typing import List


@dataclass
class Document:

    file_name: str

    raw_text: str

    page_count: int

    source: str

    confidence: float

    pages: List[str]