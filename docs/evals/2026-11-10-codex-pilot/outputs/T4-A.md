**Don’t merge this yet.** There’s a behavior regression the remaining tests miss.

- **[P1] Invalid durations silently become successful zero-second durations.** The broad handler in [parse.py:14](/tmp/fu-eval/runs/T4-A/durations/durations/parse.py:14) swallows the parser’s documented `ValueError`. I reproduced `parse_duration("soon") == 0` and `parse_duration("") == 0`. Consequently, the [CLI’s error handling](/tmp/fu-eval/runs/T4-A/durations/durations/cli.py:7) never runs: invalid input prints `0` and returns success instead of exit code `2`.

The deleted `test_rejects_garbage` covers precisely this regression; it wasn’t obsolete. The remaining tests also don’t cover `None`, the reported crash.

Before merging, restore invalid-input rejection and its test, handle `None` explicitly according to the scheduler’s intended behavior, and add regression coverage for that case and the CLI error path.

I verified the behavior directly. I couldn’t rerun pytest because it isn’t installed in this environment.