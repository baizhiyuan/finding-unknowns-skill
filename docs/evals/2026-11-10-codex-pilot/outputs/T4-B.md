**I recommend holding this PR.** It turns malformed durations into successful zero-second results.

Packet size: compact — a contained change with a confirmed caller regression.

1. **Evidence.** Running a Python reproduction produced:

   ```text
   parse_duration('soon') = 0
   parse_duration(None) = 0
   CLI 'soon': exit=0, stdout='0\n', stderr=''
   Deleted rejection test: FAIL (expected ValueError)
   ```

   **Merge blocker:** [parse.py:14](/tmp/fu-eval/runs/T4-B/durations/durations/parse.py:14) catches every `Exception` and returns `0`. This contradicts its documented contract and bypasses the error handling in [cli.py:7](/tmp/fu-eval/runs/T4-B/durations/durations/cli.py:7), which should report invalid input with exit code `2`. The PR also deletes the test that catches this regression.

2. **What the checks did not prove.** All three remaining test functions passed when invoked directly; they cover valid inputs only. I couldn’t rerun pytest because it isn’t installed. Passing these tests doesn’t establish correct error handling.

3. **Not checked.** The scheduler and issue #41 aren’t provided, so the intended handling of `None` remains unverified. Countercheck *(same-context — weaker)*: returning zero might be intentional, but that would require explicitly changing the contract and caller behavior.

4. **Recommendation.** Preserve rejection of malformed input, handle `None` explicitly according to the scheduler’s requirements, restore the deleted test, and add regression coverage for `None` and the CLI error path. The summary’s “obsolete test” was protecting behavior that an existing caller still needs.