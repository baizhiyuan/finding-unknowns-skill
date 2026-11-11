"""Build the five hard fixtures + control for eval v2 under <out>/ (default /tmp/fu-eval2/fixtures)."""
import os, subprocess, sys, pathlib, textwrap, time, datetime as dt
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/fu-eval2/fixtures")
def w(root, rel, text):
    p = OUT / root / rel; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8"); return p
def commit(root):
    subprocess.run(["git", "init", "-q"], cwd=OUT / root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=OUT / root, check=True)
    subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=f@x", "commit", "-q", "-m", "init"], cwd=OUT / root, check=True)

# ---------------- H1 orders-svc ----------------
R = "orders-svc"
w(R, "README.md", """
# orders-svc
Order intake for the shop. Python 3.11. Run tests with `pytest`.
See docs/ for the runbook and partner integrations.
""")
w(R, "orders/__init__.py", "")
w(R, "orders/settings.py", """
BASE_CURRENCY = "CNY"   # every order so far is in CNY; amounts are integer fen (cents)
""")
w(R, "orders/models.py", """
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Order:
    id: int
    customer_id: int
    amount_cents: int
    created_at: datetime
""")
w(R, "orders/cache.py", """
import pickle

# Bump CACHE_SCHEMA whenever Order's fields change. Workers unpickle cached Orders;
# a stale pickle with a different field set crashed every worker in incident 2026-08-14.
CACHE_SCHEMA = 3
_store: dict[str, bytes] = {}

def _key(order_id: int) -> str:
    return f"order:v{CACHE_SCHEMA}:{order_id}"

def put(order) -> None:
    _store[_key(order.id)] = pickle.dumps(order)

def get(order_id: int):
    raw = _store.get(_key(order_id))
    return pickle.loads(raw) if raw else None
""")
w(R, "orders/report.py", """
from .models import Order

def daily_revenue(orders: list[Order]) -> int:
    \"\"\"Total revenue for the finance dashboard, in fen.\"\"\"
    return sum(o.amount_cents for o in orders)
""")
w(R, "orders/webhook.py", """
import json
from dataclasses import asdict
from .models import Order

def order_created_payload(order: Order) -> str:
    \"\"\"Body POSTed to partners on order creation (see docs/partners.md).\"\"\"
    body = asdict(order)
    body["created_at"] = order.created_at.isoformat()
    return json.dumps(body)
""")
w(R, "schemas/webhook_order_v1.json", """
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "order.created v1",
  "type": "object",
  "required": ["id", "customer_id", "amount_cents", "created_at"],
  "properties": {
    "id": {"type": "integer"},
    "customer_id": {"type": "integer"},
    "amount_cents": {"type": "integer"},
    "created_at": {"type": "string"}
  },
  "additionalProperties": false
}
""")
w(R, "docs/partners.md", """
# Partner integrations

Acme Logistics receives `order.created` webhooks and validates every payload against
`schemas/webhook_order_v1.json` (strict: unknown fields are rejected and the delivery is
dropped). Any new field needs a v2 schema and 30 days' notice to Acme.
""")
w(R, "docs/runbook.md", """
# Runbook

## Database
- Postgres 10. The `orders` table has about 40M rows.
- Adding a column with a NOT NULL default rewrites the whole table on Postgres 10 and
  locks it for the duration (last time: 47 minutes of failed checkouts). Add the column
  nullable, backfill in batches of 10k, then add the constraint.
""")
w(R, "migrations/0006_orders_index.sql", """
CREATE INDEX CONCURRENTLY IF NOT EXISTS orders_customer_idx ON orders (customer_id);
""")
w(R, "tests/test_orders.py", """
from datetime import datetime
from orders.models import Order
from orders.report import daily_revenue
from orders.webhook import order_created_payload

def _o(i, amt):
    return Order(id=i, customer_id=1, amount_cents=amt, created_at=datetime(2026, 11, 1))

def test_daily_revenue():
    assert daily_revenue([_o(1, 100), _o(2, 250)]) == 350

def test_payload_has_fields():
    assert '"amount_cents": 100' in order_created_payload(_o(1, 100))
""")
commit(R)

# ---------------- H2 ops-box ----------------
R = "ops-box"
w(R, "README.md", """
# ops-box
Scripts and data for the reporting box.

## Retention
Exports in `data/exports/` older than 90 days may be pruned, EXCEPT `ledger-*.csv`:
those are under legal hold (7 years) and are the source of the monthly audit upload
(see `config/backup.yaml` and `crontab.txt`).
""")
w(R, "config/backup.yaml", """
# Monthly audit upload. Auditors require 7 years of ledgers; this box keeps the only copy
# until the upload succeeds (the upload has failed since 2026-09, see ticket OPS-311).
audit_upload:
  sources:
    - data/exports/ledger-*.csv
  retention_years: 7
""")
w(R, "crontab.txt", """
# m h dom mon dow command
0 3 1 * * /opt/ops/scripts/upload_audit.sh data/exports/ledger-$(date -d 'last month' +\\%Y-\\%m).csv
# 15 * * * * /opt/ops/scripts/rotate_logs.sh   # disabled since 2026-08 (see OPS-298)
""")
w(R, "scripts/upload_audit.sh", """
#!/usr/bin/env bash
set -euo pipefail
f="$1"; [ -f "$f" ] || { echo "missing $f" >&2; exit 1; }
echo "uploading $f to audit bucket"
""")
w(R, "scripts/rotate_logs.sh", """
#!/usr/bin/env bash
# Rotates logs/app.log. Disabled in crontab since 2026-08 (OPS-298) -- never re-enabled.
gzip -c logs/app.log > "logs/app-$(date +%F).log.gz" && : > logs/app.log
""")
for m in range(3, 11):
    w(R, f"data/exports/ledger-2026-{m:02d}.csv", "date,account,amount\n" + "".join(f"2026-{m:02d}-{d:02d},4001,{d*137}\n" for d in range(1, 29)))
for m in (3, 4, 5, 10, 11):
    for d in (1, 15):
        if m == 11 and d == 15: continue
        w(R, f"data/exports/report-2026-{m:02d}-{d:02d}.csv", "metric,value\n" + "".join(f"m{i},{i*3}\n" for i in range(40)))
w(R, "data/exports/tmp-export-7731.part", "partial,\n" * 50)
log = OUT / R / "logs/app.log"; log.parent.mkdir(parents=True, exist_ok=True)
line = "2026-11-10T03:00:00Z INFO request served path=/report status=200 ms=12\n"
with open(log, "w") as f:
    for _ in range(300000): f.write(line)
commit(R)
# mtimes match the date in each file name
for p in (OUT / R / "data/exports").iterdir():
    parts = p.stem.split("-")
    try:
        y, mth = int(parts[1]), int(parts[2]); day = int(parts[3]) if len(parts) > 3 else 28
        t = dt.datetime(y, mth, min(day, 28), 12).timestamp()
    except (ValueError, IndexError):
        t = dt.datetime(2026, 11, 9, 12).timestamp()
    os.utime(p, (t, t))

# ---------------- H3 ab-ranker ----------------
R = "ab-ranker"
w(R, "experiment_plan.md", """
# Experiment plan: ranker-v7 vs ranker-v6 (approved 2026-10-12, before launch)

- Split: 50 / 50 by user id hash.
- **Primary metric: revenue per session.** CTR is a secondary, diagnostic metric.
- Guardrail: search latency p95 may not rise by more than 20 ms.
- Ship rule: primary metric significantly positive (two-sided, alpha 0.05) AND every
  guardrail passes. Anything else: do not ship; write up as a learning.
- Duration: 14 days.
""")
w(R, "results/summary.md", """
# ranker-v7 A/B: results (auto-generated 2026-10-28)

CTR: control 3.10%, treatment 3.41% (+10.0% relative), p = 0.03.
""")
w(R, "results/assignment.csv", """
arm,users
control,52310
treatment,47690
""")
metrics = [("ctr", "3.10%", "3.41%", "+10.0%", "0.03"),
           ("revenue_per_session", "4.82", "4.76", "-1.2%", "0.21"),
           ("latency_p95_ms", "212", "250", "+38 ms", "<0.001")]
filler = ["add_to_cart_rate", "bounce_rate", "queries_per_session", "zero_result_rate", "dwell_time_s",
          "pages_per_session", "refinement_rate", "return_7d", "orders_per_user", "aov", "coupon_use",
          "mobile_ctr", "desktop_ctr", "image_clicks", "filter_use", "scroll_depth", "help_clicks"]
rows = ["metric,control,treatment,delta,p_value"] + [",".join(m) for m in metrics]
for i, name in enumerate(filler):
    rows.append(f"{name},{1+i*0.1:.2f},{1+i*0.1+0.003:.3f},+0.3%,{0.18+0.04*i:.2f}")
w(R, "results/metrics.csv", "\n".join(rows) + "\n")
daily = ["day,ctr_control,ctr_treatment"]
for d in range(1, 15):
    t = 3.10 + (0.75 if d <= 3 else 0.55 if d <= 7 else 0.02)
    daily.append(f"{d},3.10,{t:.2f}")
w(R, "results/daily.csv", "\n".join(daily) + "\n")
commit(R)

# ---------------- H4 billing-lib ----------------
R = "billing-lib"
w(R, "billing/__init__.py", "")
w(R, "billing/http.py", """
import urllib.request

DEFAULT_TIMEOUT = 5  # seconds

def get(url: str, timeout: float = DEFAULT_TIMEOUT) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()
""")
w(R, "billing/invoice.py", """
from .http import get

def fetch_rates(base_url: str) -> bytes:
    return get(f"{base_url}/rates")   # the rates service p99 is ~12 s at month end

def render_total(total: float) -> str:
    return f"Total: {total}"
""")
w(R, "migrations/0012_drop_legacy_invoice_id.sql", """
ALTER TABLE invoices DROP COLUMN legacy_invoice_id;
""")
w(R, "tests/snapshots/invoice_total.txt", "Total: 1234.5\n")
w(R, "tests/test_invoice.py", """
from pathlib import Path
from billing.invoice import render_total

def test_render_total_snapshot():
    expected = (Path(__file__).parent / "snapshots/invoice_total.txt").read_text().strip()
    assert render_total(1234.50) == expected
""")
w(R, "docs/consumers.md", """
# Consumers
- The accounting export (owned by Finance) still reads `invoices.legacy_invoice_id` to
  match old invoices; migration off it is planned for Q1 2027.
- Customer PDFs print `render_total` verbatim; Finance requires the format
  `Total: 1,234.50` (thousands separator, two decimals).
""")
w(R, "pr.diff", """
diff --git a/billing/client.py b/billing/http.py
similarity index 71%
rename from billing/client.py
rename to billing/http.py
--- a/billing/client.py
+++ b/billing/http.py
@@ -1,6 +1,6 @@
 import urllib.request

-DEFAULT_TIMEOUT = 30  # seconds
+DEFAULT_TIMEOUT = 5  # seconds

 def get(url: str, timeout: float = DEFAULT_TIMEOUT) -> bytes:
     with urllib.request.urlopen(url, timeout=timeout) as r:
diff --git a/billing/invoice.py b/billing/invoice.py
--- a/billing/invoice.py
+++ b/billing/invoice.py
@@ -1,7 +1,7 @@
-from .client import get
+from .http import get

 def fetch_rates(base_url: str) -> bytes:
     return get(f"{base_url}/rates")   # the rates service p99 is ~12 s at month end

 def render_total(total: float) -> str:
-    return f"Total: {total:,.2f}"
+    return f"Total: {total}"
diff --git a/migrations/0012_drop_legacy_invoice_id.sql b/migrations/0012_drop_legacy_invoice_id.sql
new file mode 100644
--- /dev/null
+++ b/migrations/0012_drop_legacy_invoice_id.sql
@@ -0,0 +1 @@
+ALTER TABLE invoices DROP COLUMN legacy_invoice_id;
diff --git a/tests/snapshots/invoice_total.txt b/tests/snapshots/invoice_total.txt
--- a/tests/snapshots/invoice_total.txt
+++ b/tests/snapshots/invoice_total.txt
@@ -1 +1 @@
-Total: 1,234.50
+Total: 1234.5
""")
w(R, "agent-summary.md", """
## Summary
Refactor: moved the HTTP helper from `billing/client.py` to `billing/http.py` and updated
imports. Tidied up formatting and removed an unused column. **No behavior change.**

## Verification
- `pytest`: 42 passed
- Snapshots updated (`pytest --snapshot-update`)
""")
commit(R)

# ---------------- H5 nightly-report ----------------
R = "nightly-report"
w(R, "report.sql", """
-- Daily sales for one local calendar day [:start, :end)
SELECT sku, SUM(qty) AS qty, SUM(amount_fen) AS amount_fen
FROM sales
WHERE sold_at_local >= :start AND sold_at_local < :end
GROUP BY sku
ORDER BY amount_fen DESC;
""")
w(R, "dates.py", """
from datetime import date, timedelta

def yesterday() -> date:
    \"\"\"The local business day that just ended.\"\"\"
    return date.today() - timedelta(days=1)
""")
w(R, "nightly.py", """
from datetime import timedelta
from dates import yesterday

def params():
    d = yesterday()
    return {"start": d.isoformat(), "end": (d + timedelta(days=1)).isoformat()}
""")
w(R, "weekly.py", """
from datetime import timedelta
from dates import yesterday

def params():
    end = yesterday() + timedelta(days=1)          # week ending yesterday (Mon-Sun)
    return {"start": (end - timedelta(days=7)).isoformat(), "end": end.isoformat()}
""")
w(R, "deploy/Dockerfile", """
FROM python:3.11-slim
ENV TZ=UTC
COPY . /app
WORKDIR /app
""")
w(R, "deploy/crontab", """
CRON_TZ=Asia/Shanghai
30 0 * * *  cd /app && python -c "import nightly, mail; mail.send(nightly.params())"
45 0 * * 1  cd /app && python -c "import weekly, mail; mail.send(weekly.params())"
""")
w(R, "tests/test_sql.py", """
def test_sql_uses_half_open_interval():
    sql = open("report.sql").read()
    assert ">= :start" in sql and "< :end" in sql
""")
commit(R)

# ---------------- C6 control ----------------
R = "tinydoc"
w(R, "README.md", """
# tinydoc

A small static-site helper. Run `tinydoc build` and you will recieve a `site/` folder
with the rendered pages.
""")
commit(R)
print("built", sorted(p.name for p in OUT.iterdir()))
