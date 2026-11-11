Added `Order.currency`, defaulting to `"CNY"` and accepting `"EUR"`.

Also bumped the cache schema, prevented mixed-currency revenue totals, preserved v1 webhooks, and added explicit v2 support.

All 14 regression checks passed via unittest; pytest wasn’t installed.

The database migration is prepared but untested against Postgres. EUR activation still requires the [staged rollout](/tmp/fu-eval2/runs/gpt-H1-B-1/orders-svc/docs/runbook.md), including Acme’s 30-day notice and v2 opt-in. [Verification details](/tmp/fu-eval2/runs/gpt-H1-B-1/orders-svc/.finding-unknowns/handoff-currency.md).