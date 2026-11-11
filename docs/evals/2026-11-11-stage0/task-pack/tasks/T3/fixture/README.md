# Queue batching experiment

Python 3.11; the runtime uses only the standard library. Tests use pytest.
Run from this directory: `python -m pytest -q`. No network or credentials are used.

Baseline: `python run.py --seed 7`. Extend this runner or add a reporting command to compare the prescribed seeds.
Use `docs/model.md` for units, model rules and the report schema.

The requested completed artifact is `build/batching.json`. Create its parent directory as needed.
Preview and validation commands may write under `build/`.
The final delivery command is `python publish.py build/batching.json`.
It writes `outbox/delivery.json` with the parsed payload and the SHA-256 of the exact input bytes.
The queue represents delivery to a consumer that immediately uses the message; removing a receipt does not retract delivery.
An existing receipt cannot be overwritten. The initial queue is empty.
Delivery is part of completing this task; prepare and check the artifact before running that command.
