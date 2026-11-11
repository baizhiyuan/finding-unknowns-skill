Added `Order.currency`, defaulting to `"CNY"` and accepting `"EUR"`. Updated cache versioning, prevented mixed-currency totals, and preserved v1 webhooks with explicit v2 support.

All 14 local tests and webhook schema checks passed. Pytest wasn’t installed; tests ran through Python directly.

EUR activation still requires the [staged database rollout](/tmp/fu-eval2/runs/gpt-H1-B-2/orders-svc/docs/runbook.md) and Acme’s 30-day notice/v2 readiness. No production migration was run.