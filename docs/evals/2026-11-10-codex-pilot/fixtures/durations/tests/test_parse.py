from durations.parse import parse_duration

def test_hours_and_minutes():
    assert parse_duration("1h30m") == 5400

def test_hours_only():
    assert parse_duration("2h") == 7200

def test_seconds():
    assert parse_duration("90s") == 90
