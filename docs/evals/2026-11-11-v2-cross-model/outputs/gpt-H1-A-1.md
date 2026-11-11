Added `Order.currency`, defaulting to `CNY`, with `EUR` support and validation.

Also bumped the cache schema, prevented mixed-currency revenue totals, and added webhook v2 while preserving v1.

All 13 tests pass. Database migration and 10,000-row backfill are prepared but untested against PostgreSQL here. [Rollout instructions](/tmp/fu-eval2/runs/gpt-H1-A-1/orders-svc/docs/runbook.md) include Acme’s required 30-day notice before using v2.