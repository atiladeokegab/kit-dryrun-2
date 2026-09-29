import unittest
from decimal import Decimal

from expenses.parse import parse


class ParseTest(unittest.TestCase):
    def test_amount_formats_and_currencies(self):
        cases = [
            ("TOTAL £12.50", "12.50", "GBP"),
            ("TOTAL 12.50 GBP", "12.50", "GBP"),
            ("TOTAL GBP 12.50", "12.50", "GBP"),
            ("TOTAL 12,50", "12.50", ""),
            ("Total due 1,234.50 GBP", "1234.50", "GBP"),
            ("AMOUNT PAID €8.40", "8.40", "€"),
            ("TOTAL USD 7.00", "7.00", "USD"),
            ("TOTAL $4.00", "4.00", "$"),
        ]
        for line, amount, currency in cases:
            with self.subTest(line=line):
                receipt = parse("r.txt", f"Cafe\n{line}")
                self.assertEqual(receipt.total, Decimal(amount))
                self.assertEqual(receipt.currency, currency)
                self.assertEqual(receipt.source, "r.txt")

    def test_last_total_like_line_wins(self):
        text = "Cafe\nSubtotal £9.00\nVAT £1.80\nTOTAL £10.80\nTotal due £11.00\nAMOUNT PAID £11.50"
        self.assertEqual(parse("r.txt", text).total, Decimal("11.50"))

    def test_subtotal_and_vat_do_not_replace_total(self):
        text = "Cafe\nTOTAL £10.80\nVAT £1.80\nSubtotal £9.00"
        self.assertEqual(parse("r.txt", text).total, Decimal("10.80"))

    def test_no_total_is_not_counted(self):
        receipt = parse("r.txt", "Cafe\nSubtotal £9.00\nVAT £1.80")
        self.assertIsNone(receipt.total)


if __name__ == "__main__":
    unittest.main()
