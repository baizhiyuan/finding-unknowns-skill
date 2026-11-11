import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CENT = Decimal("0.01")


def money(value):
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def line_total(row):
    return money(Decimal(row["quantity"]) * Decimal(row["unit_price"]))


def total(rows):
    return sum((line_total(row) for row in rows), Decimal("0.00"))


def load(path="data/lines.csv"):
    with Path(path).open(newline="") as stream:
        return list(csv.DictReader(stream))


if __name__ == "__main__":
    import json
    rows = load()
    print(json.dumps({"rows": len(rows), "credit_rows": sum(Decimal(r["quantity"]) < 0 for r in rows),
                      "line_rounded_total": str(total(rows)),
                      "once_rounded_total": str(money(sum(Decimal(r["quantity"]) * Decimal(r["unit_price"]) for r in rows)))}))
