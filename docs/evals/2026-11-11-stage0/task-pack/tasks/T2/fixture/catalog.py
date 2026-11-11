import json
from pathlib import Path


def search_key(title):
    return title.casefold()


def load(path="data/books.json"):
    return json.loads(Path(path).read_text())


if __name__ == "__main__":
    rows = load()
    print(json.dumps({"rows": len(rows), "unique_isbns": len({r["isbn"] for r in rows}),
                      "keys": [search_key(r["title"]) for r in rows]}, ensure_ascii=False))
