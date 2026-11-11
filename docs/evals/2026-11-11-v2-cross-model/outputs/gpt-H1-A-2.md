Added `Order.currency`, defaulting to `CNY`, with `EUR` support and validation.

- Revenue totals stay separate by currency.
- Cache version bumped.
- Existing v1 webhooks preserved; v2 includes currency.
- Added the database migration and batched backfill instructions.

All eight tests and webhook schema checks passed. Pytest wasn’t installed, so tests ran through Python directly.

Production EUR intake still requires the database rollout and partner v2 readiness, including Acme’s documented 30-day notice.