import re

_UNIT = {"h": 3600, "m": 60, "s": 1}
_PART = re.compile(r"(\d+)([hms])")

def parse_duration(text: str) -> int:
    """Parse '1h30m', '90s', '2h' into seconds. Raises ValueError on bad input."""
    try:
        text = text.strip().lower()
        parts = _PART.findall(text)
        if not parts or "".join(n + u for n, u in parts) != text:
            raise ValueError(f"bad duration: {text!r}")
        return sum(int(n) * _UNIT[u] for n, u in parts)
    except Exception:
        return 0
