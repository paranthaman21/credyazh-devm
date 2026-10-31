# CredYazh voice-to-ledger latency — root cause analysis

**Date:** 2026-10-28  
**Scope:** Microphone recording → WAV → Express → Python AI service → Gemini → merchant review  
**Rule used here:** only code-verified facts, previously captured incident evidence, and explicitly labeled hypotheses.

## 1. Verdict

The 11–20 second (and 21.30s) tails were **not** caused by React rendering or MongoDB. They were caused by **sequential Gemini model attempts, each with its own ~10 second HTTP timeout**, after the primary model stalled.

A timeout on `gemini-3.5-flash-lite` was treated as retryable, so `_ask` immediately started `gemini-3.5-flash` and waited again. Two independent waits stacked.

**A deadline now caps waiting. It does not make Gemini inference faster.** Successful warm requests still take however long Gemini takes (often well under 8s). Slow/stalled requests must fail into merchant review instead of waiting a second 10s.

## 2. Previously captured incident (not re-measured this session)

Source: `credyazh/docs/ai-service/FAILOVER_AUDIT_REPORT.md`, citing screenshot `docs/ai-service/evidence/manual-fallback-21s.png`.

| Observation | Value | Status |
|---|---|---|
| Client total duration | **21.30s** | Captured on review screen; not re-run this session |
| Rolling p50 in that session | **10.01s** | Same source |
| Rolling p95 in that session | **21.30s** | Same source |
| Result | `manual_fallback`, empty customer/total/items | Same source |
| UI chip | `Failover (2 models tried)` | Same source; see mislabel below |

That screenshot proves the **client waited 21.30s** and received a low-confidence empty draft after **two model attempts**. It does **not** prove Groq ran. Groq was not on the audio `_ask` path at the time of that incident.

## 3. Confirmed execution path (current source)

| Step | File | Function / handler | Latency role |
|---|---|---|---|
| Record WebM, convert 16 kHz mono WAV | `credyazh/client/src/recorder.js` | `startRecording`, `toWav` | Local CPU; not the 11–20s tail |
| Upload WAV as `FormData` | `credyazh/client/src/api.js` | `api.draftFromAudio` | Browser → Node; `upload_ms` timed |
| Duplicate-submit guard + processing UI | `credyazh/client/src/LiveVoiceModal.jsx` | `handleDone`, `processWav`, `submittingRef` | UX only |
| Multipart receive (5 MB cap) | `credyazh/server/src/routes.js` | `POST /draft/audio` | Small |
| Node → Python binary POST | `credyazh/server/src/aiClient.js` | `draftFromAudio`, `aiFetch` | `AbortSignal.timeout(AI_TIMEOUT_MS)` default **10000** |
| Decode audio bytes | `credyazh/ai-service/main.py` | `draft_audio` | `audio_decode_ms` |
| Gemini extract + fallback loop | `credyazh/ai-service/main.py` | `_ask`, `_build_config` | **Dominant** |
| Shared deadline math + error policy | `credyazh/ai-service/gemini_deadline.py` | `attempt_timeout_ms`, `should_fallback`, `classify_error` | Policy |
| Optional Groq failover (env-gated) | `credyazh/ai-service/failover_orchestrator.py` | `extract_audio`, `_execute_primary_audio`, `_execute_groq` | Only if `AI_FAILOVER_ENABLED` and budget remains |
| Merchant confirm before save | `credyazh/server/src/routes.js` | `POST /ledger` | After review; not on extract critical path |

Frontend request IDs: `client/src/api.js` (`X-Request-Id`) → `server/src/routes.js` (`requestIdOf`) → `aiClient.js` → `main.py` (`_request_id_from`).

## 4. Gemini calls, timeouts, retries (verified in source)

### 4.1 How many Gemini calls per voice note?

- **Normal success:** one `client.models.generate_content` in `_ask` (`main.py`).
- **Legacy failure path (root cause):** one call per configured model, **sequential**. Default chain:

  `GEMINI_MODELS=gemini-3.5-flash-lite,gemini-3.5-flash`

- **Speculative parallel Gemini calls:** not present. Do not add them (free-tier quota).

### 4.2 Timeouts (before vs after the policy change)

| Knob | Legacy / incident-era | Current defaults (`gemini_deadline.py` + `.env.example`) |
|---|---|---|
| Per Gemini HTTP timeout | `GEMINI_REQUEST_TIMEOUT_MS` default **10000**; live env had been **10000** | **6500**, cannot exceed remaining shared deadline |
| Shared deadline | Independent per-model waits; live env had been **12000** | `AI_SHARED_DEADLINE_MS` **8000** |
| Node → Python | `AI_CLIENT_TIMEOUT_MS` default **10000** | **10000** (must exceed 8000 so Express can return) |
| Min budget to start another attempt | Not enforced as a hard skip | `GEMINI_MIN_ATTEMPT_BUDGET_MS` **2000** |

SDK: `_build_config` sets `types.HttpOptions(timeout=…, retry_options=types.HttpRetryOptions(attempts=1))`. That **disables extra SDK retries** so a 429/503 cannot stack waits on top of the shared deadline.

Whether `HttpOptions.timeout` always cancels the in-flight Google HTTP request is **SDK/transport-dependent**. The code sets the timeout; **in-flight cancellation was not proven with a live packet capture this session.**

### 4.3 Retry / fallback policy (the actual bug)

**Confirmed in the incident-era `_ask` loop:** after a timeout/transient error, the next model in `MODELS` was started while budget still existed as a full second 10s timeout.

**Current `should_fallback` (`gemini_deadline.py`):**

| Error class | Another Gemini model? | Groq (if failover enabled and ≥2s left)? |
|---|---|---|
| `timeout` (including HTTP 504) | **No** | Yes, only if remaining budget ≥ `GEMINI_MIN_ATTEMPT_BUDGET_MS` |
| `transient` (503/500/502) | Yes, if ≥2s left | Yes |
| `rate_limit` | Yes, after bounded ≤250ms backoff if budget allows | Yes |
| `malformed` / `not_found` / `blocked` | Yes, if budget remains | Yes |
| `auth` / `invalid_request` | **No** | **No** |

This is the highest-impact fix: **waiting out a 6.5–10s Gemini timeout must not start a second Gemini wait.**

After a full 6.5s Gemini timeout, remaining shared budget is **1500ms < 2000ms**, so Groq is also skipped (`extract_audio` remaining-budget check). The merchant gets a low-confidence draft for review, not another 10s freeze.

### 4.4 Other verified contributors (not the 21s tail)

| Item | Finding |
|---|---|
| Base64 twice | Legacy JSON `audio_base64` still accepted. **Current Node path sends raw WAV bytes** (`aiClient.draftFromAudio`). Browser still uses multipart `FormData`, not Base64 JSON. |
| HTTP keep-alive Node→Python | `undici.Agent` keep-alive in `aiClient.js` when undici is available. |
| WAV convert | Required: browsers record WebM; Gemini path uses WAV (`recorder.js`). Local, not 11–20s. |
| Extra AI validation call | None. One structured JSON `GenerateContentConfig` (`response_mime_type=application/json`, `response_schema=Draft`). |
| MongoDB | Customer match happens **after** AI returns (`buildDraftResponse` in `routes.js`). Not on Gemini wait. |
| Cold start | **Hypothesis:** first request after a sleeping host can add seconds. **Not measured this session.** |
| Connection reuse Python→Gemini | Cached `genai.Client` in `main._client` and `FailoverOrchestrator._get_gemini_client`. Benefit **not measured** live. |

## 5. Hypotheses (not treated as fact)

1. Gemini multimodal audio sometimes exceeds 6.5s even when healthy — possible; **live p50/p95 this session: not measured.**
2. Render/free-tier process sleep adds cold-start latency — possible; **not measured.**
3. Groq Whisper + LLM after a *fast* Gemini 503 can still consume remaining deadline — allowed by code; **live duration not measured.**
4. `HttpOptions.timeout` always aborts the Google TCP request — intended; **not packet-verified.**

## 6. What was not the root cause

- Merchant confirmation / ledger save (happens after review).
- Invented item prices (validation still forbids guessed `price_rupees`).
- Duplicate React submissions (`submittingRef` / `busy`).
- Sequential Mongo queries as the 21s wait.

## 7. Implication for the 6–8s target

- **Wait cap (implemented):** AI shared deadline 8s; per-attempt 6.5s; no second Gemini on timeout.
- **Target achieved for live end-to-end voice notes this session:** **not measured — therefore not claimed.**
- Simulated timeout-tail wait (see `03-latency-benchmark-before-after.md`): **20s → 6.5s**. That is **policy math**, not a live Gemini run.
