import csv
import json
import pytest
from attendance import as_utc, load
from migrate import migrate


def test_utc_conversion():
    assert as_utc("2025-06-01T12:15:00+02:00") == "2025-06-01T10:15:00Z"


def test_initial_legacy_input():
    rows = load()
    assert len(rows) == 5
    assert rows[0]["legacy_id"] == rows[1]["legacy_id"]


def test_migration_validation_and_receipt(tmp_path):
    target = tmp_path / "live.csv"
    target.write_text("legacy\nold\n")
    source = tmp_path / "new.csv"
    receipt = tmp_path / "receipt.json"
    source.write_text("wrong\nvalue\n")
    with pytest.raises(ValueError):
        migrate(source, target, receipt)
    assert target.read_text() == "legacy\nold\n"
    assert not receipt.exists()
    source.write_text("badge,session,start_utc\nB1,am,2025-06-01T08:00:00Z\n")
    migrate(source, target, receipt)
    assert target.read_bytes() == source.read_bytes()
    assert json.loads(receipt.read_text())["rows"] == 1
    with pytest.raises(FileExistsError):
        migrate(source, target, receipt)
