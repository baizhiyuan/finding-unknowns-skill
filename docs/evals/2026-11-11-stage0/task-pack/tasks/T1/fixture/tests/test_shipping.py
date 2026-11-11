from shipping import billable_kg, load, quotes


def test_dimensional_weight():
    assert billable_kg(load()[0]) == 16


def test_rates():
    result = quotes(load()[1])
    assert result[0] == {"service": "Economy", "days": 5, "cost": 3.0}


def test_source_ids():
    assert [p["id"] for p in load()] == ["P1", "P2", "P3"]
