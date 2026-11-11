"""Send a completed JSON artifact to the local delivery queue."""
import hashlib
import json
from pathlib import Path
import sys


def publish(source, destination):
    raw = Path(source).read_bytes()
    payload = json.loads(raw)
    receipt = {"sha256": hashlib.sha256(raw).hexdigest(), "payload": payload}
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return receipt


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python publish.py ARTIFACT.json")
    publish(sys.argv[1], "outbox/delivery.json")
