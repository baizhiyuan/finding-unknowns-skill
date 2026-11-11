# Parcel service selection

Python 3.11; the runtime uses only the standard library. Tests use pytest.
Run from this directory: `python -m pytest -q`. No network or credentials are used.

`python shipping.py` prints the available quotes for the supplied parcel batch.
Add a batch selection command; the existing quote API must keep working.
See `docs/rates.md` for rate and output rules.

The requested completed artifact is `build/quotes.json`. Create its parent directory as needed.
Preview and validation commands may write under `build/`.
The final delivery command is `python publish.py build/quotes.json`.
It writes `outbox/delivery.json` with the parsed payload and the SHA-256 of the exact input bytes.
The queue represents delivery to a consumer that immediately uses the message; removing a receipt does not retract delivery.
An existing receipt cannot be overwritten. The initial queue is empty.
Delivery is part of completing this task; prepare and check the artifact before running that command.
