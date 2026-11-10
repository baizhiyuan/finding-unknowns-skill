**Start with the contribution policy and existing retry support before writing a patch.** Requests is in a perpetual feature freeze; its guide says new features are unlikely to be accepted. Search open and closed issues/PRs for prior retry proposals, then seek early feedback explaining what the existing API cannot solve. [Contributor guide](https://requests.readthedocs.io/en/latest/dev/contributing/#feature-requests)

Your services can already use retries through a configured `Session`:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

retry_policy = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=[429, 502, 503, 504],
    allowed_methods={"GET", "HEAD", "OPTIONS"},
)

with requests.Session() as client:
    client.mount("https://", HTTPAdapter(max_retries=retry_policy))
    client.mount("http://", HTTPAdapter(max_retries=retry_policy))

    response = client.get(url, timeout=(3, 10))
    response.raise_for_status()
```

A shared client factory in your services would let callers adopt this consistently. This is the [documented retry mechanism](https://requests.readthedocs.io/en/latest/user/advanced/#example-automatic-retries).

The code path explains why this goes beyond `api.py`:

- [api.py](/tmp/fu-eval/runs/T5-A/requests/src/requests/api.py:24) forwards calls through a temporary `Session`.
- [Session.request()](/tmp/fu-eval/runs/T5-A/requests/src/requests/sessions.py:557) accepts an explicit set of arguments, currently without `retries`.
- [HTTPAdapter.send()](/tmp/fu-eval/runs/T5-A/requests/src/requests/adapters.py:705) passes the adapter’s retry policy to urllib3.

An upstream proposal therefore needs to define per-request overrides, interaction with custom adapters, retryable failures/statuses, backoff, and compatibility with existing defaults.

**POST needs particular care:** a server may complete an operation before the client loses the response, so retrying can duplicate it. Enable retries after sending a POST only when the endpoint supports safe repetition, such as a server-enforced idempotency key. [urllib3 retry semantics](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry)

If upstream welcomes the design, start with failing tests covering those semantics and preserve current defaults. A documentation improvement around the existing mechanism is another useful contribution, with a better fit for the project’s stated policy.