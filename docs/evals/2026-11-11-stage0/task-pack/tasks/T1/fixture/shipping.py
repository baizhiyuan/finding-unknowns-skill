import csv
from pathlib import Path

SERVICES = (
    {"name": "Economy", "base": 2, "per_kg": 1, "days": 5, "zones": ["urban"]},
    {"name": "Express", "base": 5, "per_kg": 0.5, "days": 2, "zones": ["urban"]},
    {"name": "Swift", "base": 5, "per_kg": 0.5, "days": 2, "zones": ["urban"]},
)


def load(path="data/parcels.csv"):
    with Path(path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def billable_kg(parcel):
    volume = float(parcel["length_cm"]) * float(parcel["width_cm"]) * float(parcel["height_cm"])
    return max(float(parcel["weight_kg"]), volume / 5000)


def quotes(parcel):
    return [{"service": s["name"], "days": s["days"],
             "cost": round(s["base"] + s["per_kg"] * billable_kg(parcel), 2)}
            for s in SERVICES if parcel["zone"] in s["zones"]]


if __name__ == "__main__":
    import json
    print(json.dumps({p["id"]: quotes(p) for p in load()}, indent=2))
