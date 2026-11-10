## Summary
Fixed the crash reported in #41 (`parse_duration(None)` raised AttributeError in the
scheduler). `parse_duration` is now robust to any input. Cleaned up an obsolete test.

## Verification
- `pytest` — 3 passed ✅
- Manually checked `parse_duration("1h30m") == 5400`
