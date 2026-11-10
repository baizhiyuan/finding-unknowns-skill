import sys
from .parse import parse_duration

def main(argv: list[str]) -> int:
    try:
        seconds = parse_duration(argv[1])
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(seconds)
    return 0
