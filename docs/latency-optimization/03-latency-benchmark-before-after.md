# Latency benchmark — before / after

**Date:** 2026-10-28  
**Important:** This file mixes three evidence classes. They are **not** interchangeable.

1. **Previously captured live UI incident** (one session, real product).
2. **Simulated policy math** run this session (no Gemini API).
3. **Live Gemini / full PWA end-to-end** — **not measured this session.**

The 6–8 second target is **not claimed as achieved** on real voice-to-ledger requests in this session.

## 1. Previously captured live incident (before the deadline policy)

Source: `credyazh/docs/ai-service/FAILOVER_AUDIT_REPORT.md` and screenshot `manual-fallback-21s.png`. **Not re-measured on 2026-10-28.**

| Metric | Value | Notes |
|---|---|---|
| End-to-end (client, that request) | **21300 ms** | Review screen `21.30s` |
| Session rolling p50 | **10010 ms** | Same screenshot session |
| Session rolling p90 | **not reported** | — |
| Session rolling p95 | **21300 ms** | Same screenshot session |
| Max in that session | **21300 ms** | — |
| Gemini-only | **not separately exported** | Audit reconstructed ~10010 ms + ~11200 ms sequential Gemini waits |
| Outcome | `manual_fallback` | Two Gemini attempts, no save |

This is the **before** shape: independent ~10s timeouts stacked.

Operator-reported inconsistent range **11–20s** matches that mechanism (one timeout ≈10s; two ≈20s). That range is an observation from product use, not a new lab table.

## 2. Simulated policy comparison (this session — not live Gemini)

Command:

```
cd credyazh/ai-service
.\.venv\Scripts\python.exe scripts\benchmark_latency.py --repeats 20
```

Harness: `credyazh/ai-service/scripts/benchmark_latency.py`  
Models of time:

- **legacy:** `min(primary, 10000)` then, on failure, `+ min(fallback, 10000)`
- **bounded:** `gemini_deadline.attempt_timeout_ms` with deadline 8000, cap 6500, min start 2000; **no second Gemini on `timeout`**

Repeats = 20. Scenarios are **deterministic**, so p50 = p90 = p95 = max.

Printed output (verbatim):

```
SIMULATED results (not live Gemini). Repeats per scenario: 20
scenario               policy          p50      p90      p95      max
warm_success           legacy         1800     1800     1800     1800
warm_success           bounded        1800     1800     1800     1800
slow_success           legacy         5200     5200     5200     5200
slow_success           bounded        5200     5200     5200     5200
primary_timeout        legacy        20000    20000    20000    20000
primary_timeout        bounded        6500     6500     6500     6500
fast_503_then_ok       legacy         1150     1150     1150     1150
fast_503_then_ok       bounded        1150     1150     1150     1150
```

### How to read this

| Scenario | Meaning | Before (legacy) | After (bounded) |
|---|---|---|---|
| `warm_success` | Gemini returns in 1800 ms | 1800 | 1800 — **no improvement** (already fast) |
| `slow_success` | Gemini returns in 5200 ms | 5200 | 5200 — **no improvement** (still one successful call) |
| `primary_timeout` | Upstream hangs 20s | **20000** (10s + 10s) | **6500** (stop after first attempt cap) |
| `fast_503_then_ok` | 250 ms 503 then 900 ms fallback | 1150 | 1150 — fallback still allowed for transient |

**Gemini-only vs end-to-end:** this table is **AI wait policy only**. It excludes WAV encoding, upload, Express, Mongo customer match, and React. Those were **not measured** here.

**Cold-start:** **not simulated.**

## 3. Live Gemini and full end-to-end (this session)

| Measurement | Status |
|---|---|
| Warm live Gemini audio extract (p50/p90/p95/max) | **Not measured** |
| Cold-start live extract | **Not measured** |
| Gemini-only live vs full PWA e2e | **Not measured** |
| Timeout rate / failure rate on live quota | **Not measured** |
| Repeatable WAV A/B on original vs optimized with the same clips | **Not measured** (no `--live` run) |

Optional live command (consumes quota; not executed here):

```
cd credyazh/ai-service
.\.venv\Scripts\python.exe scripts\benchmark_latency.py --live path\to\representative.wav --repeats 5
```

Use the **same WAV files** for any future before/after live comparison. Log `request_id`, `metrics.gemini_request_ms`, `metrics.ai_service_total_ms`, and client `end_to_end_ms` from telemetry. Do not log API keys, audio bytes, or customer names.

Full PWA e2e additionally needs:

1. AI service on `:8000` (restarted after env change)
2. Express on `:4000`
3. Vite client
4. A merchant-length Tamil/Tanglish/English clip
5. Browser telemetry (`credyazh/client/src/telemetry.js`) or `Server-Timing`

`credyazh/server/test/gemini_latency.test.js` can check Server-Timing **only when those services are up**; it was **not run** this session.

## 4. Was the 6–8 second target achieved?

| Claim | Answer |
|---|---|
| Slow-path **wait cap** in code | Yes: 6.5s per Gemini attempt, 8s shared AI deadline, no second Gemini on timeout |
| Simulated hang/timeout wait | **6500 ms**, inside the 6–8s **wait** band |
| **Actual** end-to-end voice-to-review latency p95 ≤ 8s on live Gemini | **Unknown — not measured. Target not verified.** |
| Typical (warm success) latency improved vs before | **Unknown live.** Simulation shows **no change** when the first model already succeeds in 1.8s or 5.2s |

A deadline that fires at 6.5s on a hang **meets the wait-budget goal** and **fails extraction** into merchant review. That is not the same as “successful drafts now complete in 6–8 seconds.”

## 5. Reproducible steps (so later live numbers can be added honestly)

1. Keep `AI_SHARED_DEADLINE_MS=8000` and `GEMINI_REQUEST_TIMEOUT_MS=6500` in `credyazh/ai-service/.env`. Keep `AI_CLIENT_TIMEOUT_MS=10000` in the Node env. Restart uvicorn and Express.
2. Re-run mocked suites (section 2 of `02-code-changes-and-test-results.md`) to confirm policy.
3. Re-run `benchmark_latency.py` without `--live` to refresh the simulated table.
4. For live numbers: pick N representative WAVs (credit, payment, combined, Tamil/Tanglish/English). Run `--live` and/or the PWA mic path N times **after a warm-up request**. Record p50/p90/p95/max separately for `gemini_request_ms` and client `end_to_end_ms`. Label the table **LIVE Gemini**.
5. Do not paste live rows into this file unless they came from that procedure.

## 6. Failure and timeout rates

| Source | Failure rate | Timeout rate |
|---|---|---|
| Mocked `_ask` tests | Deterministic per test case | Deterministic per test case |
| Simulated benchmark | N/A (fixed scenarios) | `primary_timeout` is 100% timeout by construction |
| Live API this session | **Not measured** | **Not measured** |
