**The useful surprise: key rotation already exists in this checkout**, so you don’t need a new `Signer` parameter.

Start with these three pieces:

1. Read [the key rotation guide](/tmp/fu-eval/runs/T1-B/itsdangerous/docs/concepts.rst:101). Pass keys to the existing `secret_key` argument **oldest to newest**. New signatures use the last key; verification accepts any listed key.
2. Trace [Signer](/tmp/fu-eval/runs/T1-B/itsdangerous/src/itsdangerous/signer.py:128), especially `derive_key` and `verify_signature`. Then read [Serializer.make_signer](/tmp/fu-eval/runs/T1-B/itsdangerous/src/itsdangerous/serializer.py:278) to see how serializers pass the keys through. `fallback_signers` handles changes to signing settings, such as digest algorithms.
3. For your Flask app, check its version and session backend. Flask’s built-in cookie sessions support [`SECRET_KEY_FALLBACKS`](https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY_FALLBACKS):

   ```python
   # Values loaded from your secret store.
   app.config["SECRET_KEY"] = new_key
   app.config["SECRET_KEY_FALLBACKS"] = [old_key]
   ```

   This option was added in Flask 3.1. Use **3.1.1 or later**: 3.1.0 had a [signing-key selection bug](https://github.com/pallets/flask/security/advisories/GHSA-4grg-w6v8-c28g). Extensions and custom session backends need separate checking.

I ran a small example against this checkout and confirmed that old signatures remain valid, new signatures use the newest key, and removing the old key rejects its signatures.

**Your best first task is an app-level integration test:** create a session under the old key, rotate configuration, confirm that session still loads, and confirm a newly issued cookie validates with the new key alone. Decide how long to retain old keys based on session lifetime and refresh behavior; keeping a key accepts signatures made with it. The existing [rotation test](/tmp/fu-eval/runs/T1-B/itsdangerous/tests/test_itsdangerous/test_signer.py:94) is a good small example to study.