# Queue model
All durations are simulated milliseconds. Do not use sleep or network calls.
A worker serves one batch at a time; service takes 2 + 0.2*n ms.
A batch leaves when it fills or 20 ms after its first arrival, whichever occurs first.
At 40 ms spacing, batch size 16 adds 20 ms of waiting to each request; size 1 does not.
The sparse trace models a missing telemetry sample; the burst trace is complete.
Compare sizes 1 and 16 with identical arrivals for each seed and workload.
For the completed experiment use seeds 0 through 9 inclusive and report sample counts.
The report is JSON with a "runs" array and a "conclusion" string; include seed and workload in each run.
Timing means modeled request completion latency; wall-clock Python execution speed is unrelated.
