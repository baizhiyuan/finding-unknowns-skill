from decimal import Decimal
from invoice import line_total, money, total


def test_half_up():
    assert money("0.335") == Decimal("0.34")


def test_line_rounding():
    rows = [{"quantity": "1", "unit_price": "0.335"}] * 3
    assert total(rows) == Decimal("1.02")


def test_signed_credit():
    assert line_total({"quantity": "-1", "unit_price": "0.1"}) == Decimal("-0.10")
