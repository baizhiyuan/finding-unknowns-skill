import hashlib
import json
import pytest
from publish import publish


def test_delivery_receipt_and_no_overwrite(tmp_path):
    source = tmp_path / "source.json"
    source.write_text('{"ok": true}\n')
    target = tmp_path / "outbox" / "delivery.json"
    receipt = publish(source, target)
    assert receipt["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert json.loads(target.read_text())["payload"] == {"ok": True}
    with pytest.raises(FileExistsError):
        publish(source, target)
