import json
from pathlib import Path


def format_amount(cents):
    sign = ""
    return f"{sign}${abs(cents) // 100}.{abs(cents) % 100:02d}"


def render(rows):
    return "\n".join(f"{row['label']}: {format_amount(row['cents'])}" for row in rows) + "\n"


if __name__ == "__main__":
    print(render(json.loads(Path("data/activity.json").read_text())), end="")
