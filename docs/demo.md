# 30-second demo

Receipts arrive as messy text: OCR noise, `£12.50` in one and `12,50 GBP` in another, a VAT line
that looks like a total. `expenses` turns a folder of them into the month's summary.

From a clean checkout of `main`, at the repo root:

```sh
python3 -m expenses samples/
python3 -m expenses samples/ --json
```

| Time | Say and show |
|---|---|
| 0–5s | "A month of receipts, as the text our phones and inboxes give us." Show one messy file in `samples/`. |
| 5–18s | Run the first command. Point at `TOTAL`, then at a receipt with a VAT line: counted once, not twice. |
| 18–24s | Point at `Not counted:` — the EUR receipt is listed with its amount, not silently converted. |
| 24–30s | Run the second command: the same numbers as JSON, ready for a spreadsheet. |

The numbers to quote are filled in after the final run from `main` (before submit).
