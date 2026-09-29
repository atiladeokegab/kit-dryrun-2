import unittest
from decimal import Decimal

from expenses.model import Receipt
from expenses.totals import category, summarise


def r(merchant, total, currency="GBP", source="x.txt"):
    return Receipt(source, merchant, "2026-09-12", None if total is None else Decimal(total), currency)


class TotalsTest(unittest.TestCase):
    def test_each_category_and_case(self):
        for merchant, want in [("Pret A Manger", "food"), ("COFFEE HOUSE", "food"), ("Trainline", "travel"),
                               ("ryman", "office"), ("Hardware Ltd", "other"), ("THE DAILY GRIND", "food")]:
            with self.subTest(merchant=merchant):
                self.assertEqual(category(merchant), want)

    def test_gbp_sums_and_zero_categories(self):
        s = summarise([r("Tesco", "12.50"), r("TfL", "3.10"), r("Tesco", "0.10")])
        self.assertEqual(s.by_category["food"], Decimal("12.60"))
        self.assertEqual(s.by_category["office"], Decimal("0"))
        self.assertEqual(s.grand_total, Decimal("15.70"))

    def test_non_gbp_and_no_total_are_not_counted_in_order(self):
        eur, none = r("Cafe Paris", "8.00", "EUR", "a.txt"), r("", None, "", "b.txt")
        s = summarise([eur, r("Tesco", "1.00"), none])
        self.assertEqual(s.not_counted, [eur, none])
        self.assertEqual(s.grand_total, Decimal("1.00"))

    def test_decimal_is_exact(self):
        self.assertEqual(summarise([r("Tesco", "0.10"), r("Tesco", "0.20")]).grand_total, Decimal("0.30"))


if __name__ == "__main__":
    unittest.main()
