I fixed the bug in `dates.py` (not `report.sql`). I haven't committed anything.

I simulated Tuesday 00:30 Shanghai, which is Monday 16:30 UTC. `nightly.params()` now returns Monday (`2026-11-09` to `2026-11-10`) instead of Sunday. I couldn't run the repo's test because `pytest` isn't installed here. That test only checks the SQL text, which I didn't touch.

I used a fixed UTC+8 offset instead of `zoneinfo`, so the fix doesn't depend on `tzdata` being in the `python:3.11-slim` image. Shanghai has no daylight saving, so a fixed offset is safe.

**Weekly report:** `weekly.py` uses the same `yesterday()` function, so the Monday 00:45 weekly email had the same one-day error. It covered the week ending Saturday, not Sunday. It is now correct, but the numbers will differ from what recipients have been getting.

**Last night's report:** I didn't re-send it. The Tuesday report that already went out still shows Sunday's sales.