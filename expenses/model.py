"""The shared contract. Only the core changes this file."""
from dataclasses import dataclass, field
from decimal import Decimal

CATEGORIES = ("food", "travel", "office", "other")


@dataclass(frozen=True)
class Receipt:
    source: str                 # file name, e.g. "03-cafe.txt"
    merchant: str               # "" if none found
    date: str                   # ISO YYYY-MM-DD, "" if none found
    total: Decimal | None       # the receipt's TOTAL in its own currency; None if none found
    currency: str               # "GBP", or the code/symbol found; "" if unknown


@dataclass(frozen=True)
class Summary:
    by_category: dict[str, Decimal]          # GBP only, every category present
    grand_total: Decimal                     # GBP only
    not_counted: list[Receipt] = field(default_factory=list)   # non-GBP or no total
