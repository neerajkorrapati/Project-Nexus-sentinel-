from dataclasses import dataclass, field
from typing import List


@dataclass
class Invoice:

    vendor: str = ""

    invoice_number: str = ""

    invoice_date: str = ""

    currency: str = "INR"

    subtotal: float = 0.0

    gst: float = 0.0

    grand_total: float = 0.0

    errors: List[str] = field(default_factory=list)
