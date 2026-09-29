import json
import unittest
from contextlib import redirect_stderr
from decimal import Decimal
from io import StringIO

from expenses.__main__ import main, render_json, render_table
from expenses.model import Receipt, Summary


def summary():
    by = {"food": Decimal("12.50"), "travel": Decimal("0"), "office": Decimal("3.10"), "other": Decimal("0")}
    eur = Receipt("09-paris.txt", "Cafe Paris", "2026-09-12", Decimal("8.00"), "EUR")
    none = Receipt("10-blur.txt", "", "", None, "")
    return Summary(by, Decimal("15.60"), [eur, none])


class CliTest(unittest.TestCase):
    def test_table_has_every_category_and_the_total(self):
        lines = render_table(summary()).splitlines()
        self.assertEqual(lines[0].split(" | "), ["CATEGORY", "GBP"])
        self.assertIn("food     | 12.50", lines)
        self.assertIn("travel   | 0.00", lines)
        self.assertIn("TOTAL    | 15.60", lines)

    def test_not_counted_lists_source_and_reason(self):
        text = render_table(summary())
        self.assertIn("Not counted:", text)
        self.assertIn("09-paris.txt: not GBP (EUR 8.00)", text)
        self.assertIn("10-blur.txt: no total found", text)

    def test_json_uses_two_decimal_strings(self):
        out = json.loads(render_json(summary()))
        self.assertEqual(out["grand_total"], "15.60")
        self.assertEqual(out["by_category"]["travel"], "0.00")
        self.assertEqual(out["not_counted"][0], {"source": "09-paris.txt", "reason": "not GBP (EUR 8.00)"})

    def test_missing_folder_exits_2(self):
        with redirect_stderr(StringIO()) as err:
            self.assertEqual(main(["/no/such/folder"]), 2)
        self.assertIn("no such folder", err.getvalue())


if __name__ == "__main__":
    unittest.main()
