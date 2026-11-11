"""Seeded daily-demand backtest; all values are in units per day."""
import argparse
from datetime import date, timedelta
import json
import random


def series(seed):
    rng = random.Random(seed)
    start = date(2025, 1, 1)
    rows = []
    for day in range(100):
        value = 50 + day + rng.uniform(-0.2, 0.2)
        if day and day % 17 == 0:
            continue
        rows.append({"date": (start + timedelta(days=day)).isoformat(), "value": value})
    return rows


def errors(rows):
    values = [r["value"] for r in rows]
    return [{"date": rows[i]["date"], "last": abs(values[i] - values[i-1]),
             "mean5": abs(values[i] - sum(values[i-5:i]) / 5)}
            for i in range(5, len(rows))]


def experiment(seed):
    rows = series(seed)
    scored = errors(rows)
    gaps = sum((date.fromisoformat(b["date"]) - date.fromisoformat(a["date"])).days != 1
               for a, b in zip(rows, rows[1:]))
    return {"rows": len(rows), "gaps": gaps, "scored": len(scored),
            "mae": {name: sum(e[name] for e in scored) / len(scored)
                    for name in ("last", "mean5")}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps({"seed": args.seed, "results": experiment(args.seed)}, indent=2))
