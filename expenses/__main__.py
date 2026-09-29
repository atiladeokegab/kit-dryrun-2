"""python3 -m expenses FOLDER [--json]"""
import argparse
import json
import sys
from pathlib import Path

from expenses.model import CATEGORIES, Summary


def reason(r):
    return "no total found" if r.total is None else f"not GBP ({r.currency or 'unknown'} {r.total})"


def render_table(s: Summary):
    rows = [("CATEGORY", "GBP")] + [(c, f"{s.by_category.get(c, 0):.2f}") for c in CATEGORIES]
    rows.append(("TOTAL", f"{s.grand_total:.2f}"))
    width = max(len(a) for a, _ in rows)
    lines = [f"{a.ljust(width)} | {b}" for a, b in rows]
    if s.not_counted:
        lines += ["", "Not counted:"] + [f"  {r.source}: {reason(r)}" for r in s.not_counted]
    return "\n".join(lines)


def render_json(s: Summary):
    return json.dumps({
        "by_category": {c: f"{s.by_category.get(c, 0):.2f}" for c in CATEGORIES},
        "grand_total": f"{s.grand_total:.2f}",
        "not_counted": [{"source": r.source, "reason": reason(r)} for r in s.not_counted],
    }, indent=2)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="expenses", description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--version", action="version", version="expenses 0.1")
    a = ap.parse_args(argv)
    folder = Path(a.folder)
    if not folder.is_dir():
        print(f"expenses: no such folder: {a.folder}", file=sys.stderr)
        return 2
    # The areas are imported here so the core works before they exist.
    from expenses.parse import parse
    from expenses.totals import summarise

    receipts = [parse(f.name, f.read_text(encoding="utf-8", errors="replace"))
                for f in sorted(folder.glob("*.txt"))]
    s = summarise(receipts)
    print(render_json(s) if a.json else render_table(s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
