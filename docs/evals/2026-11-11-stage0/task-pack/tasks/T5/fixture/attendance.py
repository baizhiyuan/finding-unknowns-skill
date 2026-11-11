import csv
from datetime import datetime, timezone
from pathlib import Path


def load(path="data/attendance.csv"):
    with Path(path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def as_utc(value):
    return datetime.fromisoformat(value).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def inspect(rows):
    keys = [(r["badge"], r["session"]) for r in rows]
    return {"rows": len(rows), "unique_legacy_ids": len({r["legacy_id"] for r in rows}),
            "duplicate_pairs": len(keys) - len(set(keys)),
            "changed_dates": [r["legacy_id"] for r in rows if r["started_at"][:10] != as_utc(r["started_at"])[:10]]}


if __name__ == "__main__":
    import json
    print(json.dumps(inspect(load()), indent=2))
