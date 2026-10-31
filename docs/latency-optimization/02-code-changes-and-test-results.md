# Code changes and test results

**Date:** 2026-10-28  
**Constraint:** financial correctness, merchant confirmation before save, no speculative parallel Gemini, no live quota in unit tests.

## 1. What was implemented

These changes address the sequential Gemini timeout stack. They **limit waiting**; they do not accelerate a healthy Gemini call.

### 1.1 Shared deadline and fallback policy

| File | Change |
|---|---|
| `credyazh/ai-service/gemini_deadline.py` | Shared deadline math (`attempt_timeout_ms`, `should_start_attempt`, `remaining_ms`). `should_fallback("timeout")` is **false**. HTTP **504** classified as timeout (not a second Gemini wait). `should_failover_provider` still allows Groq on timeout **if** ≥2s remains. Rate-limit backoff skipped when it would exhaust the deadline. |
| `credyazh/ai-service/main.py` | `_ask` uses remaining-budget timeouts. `_build_config` sets `HttpRetryOptions(attempts=1)`, `max_output_tokens`, structured JSON schema. `classify_error` lives in `gemini_deadline.py`. Request IDs and attempt logs (model, attempt, duration, timeout, status) without audio or keys. |
| `credyazh/ai-service/failover_orchestrator.py` | Same per-attempt caps; skip next Gemini on `should_fallback` false; reuse one `genai.Client`; Groq only if remaining budget ≥ `GEMINI_MIN_ATTEMPT_BUDGET_MS`. Trace separator normalized to ASCII `->`. |

### 1.2 Node / transport

| File | Change |
|---|---|
| `credyazh/server/src/aiClient.js` | `AI_CLIENT_TIMEOUT_MS` default **10000**. Binary WAV POST. Optional undici keep-alive. `X-Request-Id`. `node_to_python_ms` on metrics. |
| `credyazh/server/src/routes.js` | Propagates request id, Server-Timing, `nodeProcessingMs`, Gemini/fallback/retry/parse/audio-decode metrics. |
| `credyazh/server/.env.example` | Documents `AI_CLIENT_TIMEOUT_MS=10000`. |

### 1.3 Configuration (no secrets)

| Variable | Default / example | Meaning |
|---|---|---|
| `AI_SHARED_DEADLINE_MS` | 8000 | Total wait for one extraction |
| `GEMINI_REQUEST_TIMEOUT_MS` | 6500 | Per-attempt cap |
| `GEMINI_MIN_ATTEMPT_BUDGET_MS` | 2000 | Do not start another attempt below this |
| `GEMINI_RATE_LIMIT_BACKOFF_MS` | 250 | Short wait before justified retry |
| `GEMINI_MAX_OUTPUT_TOKENS` | 1024 | Bound output size |
| `AI_CLIENT_TIMEOUT_MS` | 10000 | Express abort; must exceed 8000 |

Documented in `credyazh/ai-service/.env.example`. Live `.env` values were aligned to 8000/6500; **API keys are not recorded here.**

### 1.4 Frontend (no redesign)

| File | Change |
|---|---|
| `credyazh/client/src/api.js` | Request IDs; `upload_ms`; FormData WAV (not Base64 JSON). |
| `credyazh/client/src/telemetry.js` | Stores `requestId` with latency samples. |
| `credyazh/client/src/LiveVoiceModal.jsx` | `submittingRef` duplicate guard; Retry; Cancel / Enter Manually. Copy no longer says CredYazh will “keep trying” through stacked Gemini waits. |
| `credyazh/client/src/App.jsx` | `busy` guard; encoding + e2e telemetry fields. |

Ledger confirm, customer matching, and amount validation (`credyazh/server/src/validate.js`) were **not** rewritten for speed.

### 1.5 Tests and harness added

| File | Role |
|---|---|
| `credyazh/ai-service/tests/test_gemini_deadline.py` | Deadline math + error classes (**mocked**, no API) |
| `credyazh/ai-service/tests/test_ask_deadline.py` | `_ask` behavior with MagicMock Gemini (**mocked**) |
| `credyazh/server/test/ai_timeout_config.test.js` | Node timeout ≥ 10s |
| `credyazh/ai-service/scripts/benchmark_latency.py` | Simulated policy comparison; optional `--live` WAV (not run this session) |

## 2. Tests executed this session (actual results)

Command working directory: `credyazh/ai-service` unless noted. Interpreter: project `.venv\Scripts\python.exe`.

### 2.1 Mocked Python (no Gemini quota)

```
.\.venv\Scripts\python.exe -m unittest tests.test_gemini_deadline tests.test_ask_deadline tests.test_failover_incident -v
```

**Result: 23 tests, OK, 0.052s.**

| Module | Tests | Outcome |
|---|---|---|
| `tests.test_gemini_deadline` | 7 | all `ok` |
| `tests.test_ask_deadline` | 9 | all `ok` |
| `tests.test_failover_incident` | 7 | all `ok` |

Behaviors covered by **mocks** (not live Gemini):

- Primary success → one `generate_content` call; HTTP retry attempts = 1
- Primary timeout → **no second Gemini**; `manual_fallback`, empty customer/total
- Fast 503 → second Gemini within deadline
- Transient that consumes 6.6s of an 8s budget → **no** second attempt (`deadline_exhausted`)
- 400 invalid_request → no retry
- Malformed JSON → next model
- 429 → bounded `time.sleep` then fallback
- Combined payment + credit JSON preserved (`kind=combined`, payment 200, credit 70, item `price_rupees` null)
- Auth 401 → HTTPException, no fallback
- Groq failover matrix (Gemini 503 / timeout / both fail / malformed Groq JSON) with mocked HTTP

### 2.2 Node unit tests (no live AI service)

```
cd credyazh/server
node --test test/ai_timeout_config.test.js test/validate.test.js
```

**Result: 10 pass, 0 fail, duration_ms 151.0271.**

Includes amount/paise rules, combined repayment+credit validation, and `AI_TIMEOUT_MS >= 10000`.

### 2.3 Not run this session (require live stack and/or quota)

| Test | Why skipped | Result |
|---|---|---|
| `credyazh/server/test/gemini_latency.test.js` | Hits `localhost:8000` and `localhost:4000` plus Gemini | **Not run** |
| `credyazh/server/test/combined_live_api.test.js` | Live API | **Not run** |
| `python scripts/benchmark_latency.py --live <wav>` | Consumes Gemini quota | **Not run** |

Do not treat skipped live tests as passes or as latency proof.

## 3. Correctness preserved (as far as tests show)

- Timeouts return a **low-confidence empty draft** for merchant review; they do **not** auto-save ledger rows.
- Combined payment + credit mock draft kept both operations and did not invent item prices.
- `validate.test.js` still enforces positive integer totals and combined-operation rules.

## 4. Risks still open

- Live Gemini may still exceed 6.5s on a **successful** audio extract. The code will wait up to the attempt cap, then stop — **speed of a healthy call is unmeasured here.**
- If `AI_FAILOVER_ENABLED=true` and Gemini fails **quickly**, Groq Whisper + LLM may use remaining budget. That can help correctness; it is **not** a second 10s Gemini timeout, but live Groq audio time was **not measured**.
- Restart the AI process after env changes (`AI_SHARED_DEADLINE_MS=8000`, `GEMINI_REQUEST_TIMEOUT_MS=6500`) or the old 10s/12s process settings remain in memory.
