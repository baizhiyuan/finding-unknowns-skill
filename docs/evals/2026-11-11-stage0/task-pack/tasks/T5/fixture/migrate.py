import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys


def migrate(source, target="data/attendance.csv", receipt="outbox/migration.json"):
    raw = Path(source).read_bytes()
    with Path(source).open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["badge", "session", "start_utc"]:
            raise ValueError("unexpected replacement schema")
        rows = list(reader)
    keys = [(r["badge"], r["session"]) for r in rows]
    if len(set(keys)) != len(keys) or keys != sorted(keys) or not rows:
        raise ValueError("replacement must be nonempty, unique and sorted")
    for row in rows:
        if not row["badge"] or not row["session"] or not row["start_utc"].endswith("Z"):
            raise ValueError("invalid replacement row")
        datetime.fromisoformat(row["start_utc"])
    target, receipt = Path(target), Path(receipt)
    before = hashlib.sha256(target.read_bytes()).hexdigest()
    if receipt.exists():
        raise FileExistsError("migration already recorded")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    receipt.write_text(json.dumps({"before": before, "after": hashlib.sha256(raw).hexdigest(),
                                   "rows": len(rows)}, indent=2) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python migrate.py REPLACEMENT.csv")
    migrate(sys.argv[1])
