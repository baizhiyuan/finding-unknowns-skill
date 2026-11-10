**Key rotation is already implemented in this checkout**, with support added in ItsDangerous 2.0. You can use it without adding a `Signer` parameter.

Start with these files:

- [docs/concepts.rst](/tmp/fu-eval/runs/T1-A/itsdangerous/docs/concepts.rst:101): explains key rotation.
- [src/itsdangerous/signer.py](/tmp/fu-eval/runs/T1-A/itsdangerous/src/itsdangerous/signer.py:67): `_make_keys_list` accepts one key or an iterable. `derive_key()` defaults to the last key, and `verify_signature()` tries keys newest to oldest.
- [src/itsdangerous/serializer.py](/tmp/fu-eval/runs/T1-A/itsdangerous/src/itsdangerous/serializer.py:278): `make_signer()` passes the serializer’s key list to its signer.
- [tests/test_itsdangerous/test_signer.py](/tmp/fu-eval/runs/T1-A/itsdangerous/tests/test_itsdangerous/test_signer.py:107): `test_secret_keys` demonstrates accepting an old signature after rotation.

Here’s the basic behavior, using example keys:

```python
from itsdangerous import Signer

old_token = Signer("old-key").sign(b"user-id=42")

signer = Signer(["old-key", "new-key"])  # oldest to newest
assert signer.unsign(old_token) == b"user-id=42"

new_token = signer.sign(b"user-id=42")  # signed with new-key
```

I verified this behavior against the local source, including rejection of old signatures once the old key is removed.

**For your Flask app**, Flask 3.1+ supports rotation for its built-in cookie sessions through [`SECRET_KEY_FALLBACKS`](https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY_FALLBACKS):

```python
import os

app.config["SECRET_KEY"] = os.environ["NEW_SECRET_KEY"]
app.config["SECRET_KEY_FALLBACKS"] = [os.environ["OLD_SECRET_KEY"]]
```

Keep the old key available until sessions signed with it have expired or been reissued with the new key. Extensions that use `SECRET_KEY` may need separate support, so check your session implementation and extensions too. Your first step should be checking your Flask version and configuration; this checkout already has the ItsDangerous functionality you need.