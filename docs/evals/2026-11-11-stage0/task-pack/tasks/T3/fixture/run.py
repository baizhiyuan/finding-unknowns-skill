"""Offline queue experiment: modeled milliseconds, not wall-clock timings."""
import argparse
import json
import math
import random


def arrivals(seed, workload):
    rng = random.Random(seed)
    if workload == "sparse":
        return [i * 40 + rng.uniform(0, 1) for i in range(32) if i != 17]
    return [i * 0.1 + rng.uniform(0, 0.01) for i in range(32)]


def latencies(times, size):
    result = []
    cursor = 0
    free_at = 0.0
    while cursor < len(times):
        batch = [times[cursor]]
        deadline = times[cursor] + 20.0
        cursor += 1
        while cursor < len(times) and len(batch) < size and times[cursor] <= deadline:
            batch.append(times[cursor])
            cursor += 1
        dispatch = batch[-1] if len(batch) == size else deadline
        finish = max(dispatch, free_at) + 2.0 + 0.2 * len(batch)
        result.extend(finish - arrival for arrival in batch)
        free_at = finish
    return result


def summarize(values):
    return {"count": len(values), "mean_ms": sum(values) / len(values),
            "p95_ms": sorted(values)[math.ceil(0.95 * len(values)) - 1]}


def experiment(seed):
    return {w: {str(size): summarize(latencies(arrivals(seed, w), size))
                for size in (1, 16)} for w in ("sparse", "burst")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps({"seed": args.seed, "results": experiment(args.seed)}, indent=2))
