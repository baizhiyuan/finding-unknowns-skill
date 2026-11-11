from run import arrivals, experiment, latencies, summarize


def test_single_request():
    assert latencies([0], 1) == [2.2]
    assert latencies([0], 16) == [22.2]


def test_reproducible():
    assert arrivals(7, "burst") == arrivals(7, "burst")


def test_summary():
    assert summarize([1, 2, 3])["p95_ms"] == 3


def test_workloads():
    assert set(experiment(7)) == {"sparse", "burst"}
