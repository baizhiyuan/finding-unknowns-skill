I added `currency` to `Order`. It wasn't quite a one-line change, because the repo has several guards that a plain field addition would have broken. pytest isn't installed here, so I called the four test functions directly and they pass. I haven't run the migration against a database.

- **Model** (`orders/models.py`): `currency: str = BASE_CURRENCY` is now the last field, so existing `Order(...)` calls still work and default to CNY.
- **Migration** (`migrations/0007_orders_currency.sql`): the column is added nullable with no default, as `docs/runbook.md` requires. A `NOT NULL DEFAULT` on the 40M-row Postgres 10 table would lock it, and the last time that happened checkouts failed for 47 minutes. Existing rows stay NULL, which means CNY.
- **Webhook** (`orders/webhook.py`): the payload leaves `currency` out. Acme's v1 schema rejects unknown fields and drops the delivery, and `docs/partners.md` says a new field needs a v2 schema and 30 days' notice. Without this, every `order.created` webhook to Acme would have been dropped.
- **Cache** (`orders/cache.py`): `CACHE_SCHEMA` goes from 3 to 4, as the comment there asks, so workers don't unpickle old Orders with a different field set.
- **Revenue report** (`orders/report.py`): `daily_revenue` would have added EUR cents to CNY fen. It now counts only CNY orders, and a new `daily_revenue_by_currency` gives per-currency totals.
- **Tests:** I added tests for the webhook payload and for the currency split in revenue.

Still to do:
1. **Backfill and constraint:** these are separate steps. Backfill `currency = 'CNY'` in batches of 10k, then add the constraint.
2. **Acme:** a v2 webhook schema and the 30 days' notice are needed before EUR orders can reach them with a currency. Until then they get EUR amounts with no currency, so they will read them as CNY. You may want to hold off sending EUR orders to them until v2 is in place.
3. **Finance dashboard:** `daily_revenue` now leaves EUR out, so finance needs to switch to `daily_revenue_by_currency` or decide how to convert.
4. **Order loading:** no code in the repo reads orders from the DB. Whatever does that should map NULL to CNY.

I haven't committed anything.