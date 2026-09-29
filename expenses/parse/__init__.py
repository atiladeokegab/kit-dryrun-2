"""Turn one receipt text dump into a Receipt."""
import re
from decimal import Decimal

from expenses.model import Receipt

_TOTAL = re.compile(r"^\s*(?:total(?:\s+due)?|amount\s+paid)\b", re.I)
_AMOUNT = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d{2})?|\d+(?:[.,]\d{2})?")
_CURRENCY = re.compile(r"\b(?:GBP|EUR|USD)\b|[£€$]", re.I)


def parse(source: str, text: str) -> Receipt:
    total = None
    currency = ""
    for line in text.splitlines():
        label = _TOTAL.match(line)
        if not label:
            continue
        amount = _AMOUNT.search(line[label.end():])
        if not amount:
            continue
        value = amount.group().replace(",", "" if "." in amount.group() else ".")
        total = Decimal(value)
        marker = _CURRENCY.search(line)
        currency = marker.group().upper() if marker else ""
        if currency == "£":
            currency = "GBP"
    if not currency:
        marker = _CURRENCY.search(text)
        currency = marker.group().upper() if marker else ""
        if currency == "£":
            currency = "GBP"
    return Receipt(source, "", "", total, currency)
