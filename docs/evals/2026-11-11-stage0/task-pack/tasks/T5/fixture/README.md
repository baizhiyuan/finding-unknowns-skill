# Attendance table migration

Python 3.11; the runtime uses only the standard library. Tests use pytest.
Run from this directory: `python -m pytest -q`. No network or credentials are used.

Normalize and deduplicate the legacy attendance table, then replace the local live table using the provided migration tool.
Schema and commands are in `docs/schema.md`. The baseline input test describes the legacy state; update it when the table is migrated.
