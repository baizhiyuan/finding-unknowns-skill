import json
from pathlib import Path
import pytest
from render import format_amount, render


@pytest.mark.parametrize("cents", range(41))
def test_nonnegative_amounts(cents):
    assert format_amount(cents) == f"$0.{cents:02d}"


def test_activity_snapshot():
    rows = json.loads(Path("data/activity.json").read_text())
    assert render(rows) == Path("tests/snapshots/activity.txt").read_text()
