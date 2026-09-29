"""Categories and the GBP summary."""
from decimal import Decimal

from expenses.model import CATEGORIES, Summary

KEYWORDS = {
    "food": ("cafe", "coffee", "espresso", "grind", "bean", "bakery", "pret", "tesco", "sainsbury", "restaurant"),
    "travel": ("trainline", "tfl", "uber", "rail", "taxi"),
    "office": ("staples", "ryman", "printer", "paper"),
}


def category(merchant: str) -> str:
    m = (merchant or "").lower()
    for name in CATEGORIES:
        if any(k in m for k in KEYWORDS.get(name, ())):
            return name
    return "other"


def summarise(receipts):
    by = {c: Decimal("0") for c in CATEGORIES}
    not_counted = []
    for r in receipts:
        if r.total is None or r.currency != "GBP":
            not_counted.append(r)
            continue
        by[category(r.merchant)] += r.total
    return Summary(by, sum(by.values(), Decimal("0")), not_counted)
