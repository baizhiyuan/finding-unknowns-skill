Start with the existing retry support and an upstream discussion. **This is broader than a small `api.py` change.**

Three findings change the approach:

1. **Retries already exist.** Requests documents `Session` + `HTTPAdapter(max_retries=Retry(...))`, including backoff and status-based retries. Your proposed keyword would make that capability easier to access. [Existing recipe](https://requests.readthedocs.io/en/latest/user/advanced/#example-automatic-retries)

2. **`api.py` only forwards calls.** The path is `get/post → request → Session.request → Session.send → HTTPAdapter.send → urllib3`. Retry policy reaches urllib3 in [adapters.py](/tmp/fu-eval/runs/T5-B/requests/src/requests/adapters.py:705). A consistent per-call keyword needs decisions about session policy, redirects, custom adapters, and typing—not just the convenience functions.

3. **Acceptance and POST behavior are the biggest unknowns.** Requests’ contribution guide declares a perpetual feature freeze and recommends early feedback. Separately, retrying after sending a POST can duplicate an operation: a lost response doesn’t mean the server failed to process it. urllib3 distinguishes connection failures from errors after sending and excludes POST from its default retry method set. [Contribution policy](https://requests.readthedocs.io/en/latest/dev/contributing/#feature-requests), [Retry semantics](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry)

For your services, you can start today with a shared session factory:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

policy = Retry(
    total=3,
    backoff_factor=0.2,
    status_forcelist=[502, 503, 504],
    allowed_methods={"GET", "HEAD", "OPTIONS"},
)

with requests.Session() as client:
    client.mount("https://", HTTPAdapter(max_retries=policy))
    response = client.get("https://example.com", timeout=(3, 10))
    response.raise_for_status()
```

This permits up to three retries beyond the initial attempt. Keep POST read/status retries out until the endpoint’s idempotency contract makes replay safe.

**My recommended first contribution:** improve the existing retry documentation with safe-method guidance and a POST replay caveat. If you still want the keyword, search open and closed issues, then seek early feedback with this narrower proposal:

> Could Requests expose its existing adapter retry policy per call? I’d preserve current defaults and define policy precedence, eligible failures and methods, and custom-adapter compatibility before implementing.

The existing [retry test](/tmp/fu-eval/runs/T5-B/requests/tests/test_requests.py:2740) is a useful starting point once the proposed behavior has support.