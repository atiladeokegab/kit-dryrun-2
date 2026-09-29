# The idea

The lead writes this once the team has agreed the idea, and no issue is created before it is
complete. If your task doesn't fit this page, open a change-request (AGENTS.md §7).

## Problem

Receipts pile up as photos and emails that become messy text: OCR noise, `£12.50` in one,
`12,50 GBP` in another, a VAT line that looks like a total. Adding them up by hand at month end
takes an hour and gets the total wrong.

## The idea

`expenses` is a command-line tool: point it at a folder of receipt text files and it reads each
one, finds the merchant, date and total, puts it in a category, and prints per-category
subtotals and a grand total in pounds. Receipts in another currency are listed as not counted.

## What we build

- Parse a messy receipt: merchant, date, total (the TOTAL, not VAT or subtotal lines)
- Category by merchant keywords (food, travel, office, other)
- `python3 -m expenses FOLDER` prints a table and the grand total; `--json` prints JSON
- A sample folder of receipts covering the messy cases

## What we don't build

- OCR from images (input is text)
- Currency conversion (non-GBP receipts are flagged, not converted)
- Any dependency outside the Python standard library

## The demo, in one line

`python3 -m expenses samples/` turns 10 tangled receipts into a four-line summary and the right total.

## Areas and owners

Each person owns their area's directories outright (AGENTS.md §6). The core is the shared
contracts; only the lead changes it.

| Area | Directories | Owner | Issues |
|---|---|---|---|
| core | `expenses/__init__.py`, `expenses/__main__.py`, `expenses/model.py`, `tests/__init__.py`, `tests/test_cli.py` | @atiladeokegab (Zeus builds) | #1 |
| parse | `expenses/parse/`, `tests/parse/` | @Atilmatrix | #2 |
| totals | `expenses/totals/`, `tests/totals/` | @atiladeokegab (Zeus builds) | #3 |
| pool (claimed) | `samples/` | @Atilmatrix | #4 |
| demo | `docs/demo.md` | @atiladeokegab (Zeus builds) | #5 |
