from run import errors, series


def test_trend_sanity():
    rows = [{"date": str(i), "value": float(i)} for i in range(6)]
    assert errors(rows) == [{"date": "5", "last": 1.0, "mean5": 3.0}]


def test_seed_repeatability():
    assert series(7) == series(7)
    assert series(7) != series(8)


def test_only_past_values():
    rows = [{"date": str(i), "value": float(i)} for i in range(7)]
    first = errors(rows)[0]
    rows[-1]["value"] = 99999
    assert errors(rows)[0] == first
