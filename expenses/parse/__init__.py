"""Turn one receipt text dump into a Receipt."""
import re
from datetime import datetime
from decimal import Decimal

from expenses.model import Receipt

_TOTAL = re.compile(r"^\s*(?:total(?:\s+(?:due|charged|paid))?|amount\s+(?:paid|charged))\b\s*:?\s*(?=(?:[£€$]|\b(?:GBP|EUR|USD)\b|\d))", re.I)
_AMOUNT = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d{2})?|\d+(?:[.,]\d{2})?")
_CURRENCY = re.compile(r"\b(?:GBP|EUR|USD)\b|[£€$]", re.I)
_DATES = (
    (re.compile(r"\b\d{4}-\d{2}-\d{2}\b"), "%Y-%m-%d"),
    (re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b"), "%d/%m/%Y"),
    (re.compile(r"\b\d{1,2} [A-Za-z]{3,9} \d{4}\b", re.I), "%d %b %Y"),
)
_AMOUNT_LINE = re.compile(r"^(?:[£€$]|(?:GBP|EUR|USD)\s*)?\d[\d,]*(?:[.,]\d{2})?\s*(?:GBP|EUR|USD)?$", re.I)
# ponytail: Flag obvious OCR artifacts; broaden only for confirmed receipt formats.
_OCR_NOISE = re.compile(r"^[#*~|?]{2,}|\b[A-Za-z]+\d+[A-Za-z]+\b")


def _date(line: str) -> str:
    for pattern, fmt in _DATES:
        match = pattern.search(line)
        if match:
            try:
                return datetime.strptime(match.group(), fmt).date().isoformat()
            except ValueError:
                pass
    return ""


def parse(source: str, text: str) -> Receipt:
    lines = text.splitlines()
    total = None
    currency = ""
    for line in lines:
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

    date = ""
    merchant = ""
    for line in lines:
        clean = line.strip()
        if not date:
            date = _date(clean)
        if merchant or not clean or not re.search(r"[A-Za-z]", clean):
            continue
        if (_date(clean) or clean.upper() in {"RECEIPT", "TAX INVOICE", "GBP", "EUR", "USD"}
                or re.match(r"^\d+(?:\s*-\s*\d+)?\s+\w", clean) or _TOTAL.match(clean)
                or re.match(r"^(?:subtotal|vat|tax)\b", clean, re.I)
                or _AMOUNT_LINE.fullmatch(clean) or _OCR_NOISE.search(clean)):
            continue
        merchant = clean
    noise_lines = sum(bool(_OCR_NOISE.search(line.strip())) for line in lines)
    notes = f"OCR noise on {noise_lines} line{'s' if noise_lines != 1 else ''}" if noise_lines else ""
    return Receipt(source, merchant, date, total, currency, notes)
