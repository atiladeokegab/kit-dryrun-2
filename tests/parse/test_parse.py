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

    def test_total_items_is_not_a_money_total(self):
        text = "Cafe\nTOTAL £12.50\nTOTAL ITEMS 2"
        self.assertEqual(parse("r.txt", text).total, Decimal("12.50"))

    def test_subtotal_and_vat_do_not_replace_total(self):
        text = "Cafe\nTOTAL £10.80\nVAT £1.80\nSubtotal £9.00"
        self.assertEqual(parse("r.txt", text).total, Decimal("10.80"))

    def test_no_total_is_not_counted(self):
        receipt = parse("r.txt", "Cafe\nSubtotal £9.00\nVAT £1.80")
        self.assertIsNone(receipt.total)

    def test_date_formats_become_iso(self):
        for date in ("2026-09-12", "12/09/2026", "12 Sep 2026"):
            with self.subTest(date=date):
                self.assertEqual(parse("r.txt", f"Cafe\n{date}\nTOTAL £5.00").date, "2026-09-12")

    def test_missing_or_invalid_date_is_empty(self):
        self.assertEqual(parse("r.txt", "Cafe\nTOTAL £5.00").date, "")
        self.assertEqual(parse("r.txt", "Cafe\n31/02/2026\nTOTAL £5.00").date, "")

    def test_merchant_skips_dates_addresses_and_amounts(self):
        text = "  \n12/09/2026\n12 High Street\n£7.00\n  Blue Cafe  \nTOTAL £7.00"
        self.assertEqual(parse("r.txt", text).merchant, "Blue Cafe")

    def test_merchant_skips_numbered_street_range(self):
        text = "12-14 High Street\nBlue Cafe\nTOTAL £5.00"
        self.assertEqual(parse("r.txt", text).merchant, "Blue Cafe")

    def test_merchant_skips_ocr_noise_and_receipt_header(self):
        text = "### 8? ###\nRECEIPT\nCorner Cafe\nTotal due £4.20"
        self.assertEqual(parse("r.txt", text).merchant, "Corner Cafe")

    def test_merchant_skips_lettered_ocr_noise(self):
        text = "### OCR NOISE ###\nCorner Cafe\nTOTAL £4.20"
        self.assertEqual(parse("r.txt", text).merchant, "Corner Cafe")

    def test_missing_merchant_is_empty(self):
        text = "###\n12/09/2026\n12 High Street\nTOTAL £5.00"
        self.assertEqual(parse("r.txt", text).merchant, "")


if __name__ == "__main__":
    unittest.main()
