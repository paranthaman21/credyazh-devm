"""CredYazh AI service.

It turns a spoken (or typed) sentence into a *draft* transaction. It does not know
about the database and never saves anything. The Express API validates the draft and
the merchant confirms it.
"""

import logging
import os
import time
import uuid
import base64
from typing import Literal, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from pydantic import BaseModel, ValidationError
from google.genai import types

from gemini_deadline import (
    attempt_timeout_ms,
    classify_error,
    rate_limit_backoff_ms,
    remaining_ms,
    should_fallback,
    should_start_attempt,
)

load_dotenv()

logger = logging.getLogger("ai_service")
logging.basicConfig(level=logging.INFO)

# Default extraction chain: fast non-thinking models only.
# gemini-3.7-flash and gemini-3.8-flash are thinking models; they incur 30–60 s
# latency on structured JSON extraction and are NOT suitable as sync extraction fallbacks.
# Add them here only if you have confirmed they are fast enough for your use-case.
raw_models = os.getenv("GEMINI_MODELS", "gemini-3.5-flash-lite,gemini-3.5-flash")
MODELS = [m.strip() for m in raw_models.split(",") if m.strip()]
if not MODELS:
    MODELS = ["gemini-3.5-flash-lite", "gemini-3.5-flash"]

# ── Timing / deadline constants (read from .env after load_dotenv) ────────────
SHARED_DEADLINE_MS: int = int(os.getenv("AI_SHARED_DEADLINE_MS", "8000"))
REQUEST_TIMEOUT_MS: int = int(os.getenv("GEMINI_REQUEST_TIMEOUT_MS", "6500"))
MIN_ATTEMPT_BUDGET_MS: int = int(os.getenv("GEMINI_MIN_ATTEMPT_BUDGET_MS", "2000"))
RATE_LIMIT_BACKOFF_MS: int = int(os.getenv("GEMINI_RATE_LIMIT_BACKOFF_MS", "250"))
MAX_OUTPUT_TOKENS: int = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "1024"))

logger.info(
    f"Initialized Gemini models: primary='{MODELS[0]}', fallbacks={MODELS[1:]}; "
    f"shared_deadline_ms={SHARED_DEADLINE_MS}, per_attempt_timeout_ms={REQUEST_TIMEOUT_MS}"
)

# Deterministic local regex fast-path for common Tamil/Tanglish/English structured notes.
# Completes in < 2 ms and avoids Gemini round-trips for simple transactions.
ENABLE_LOCAL_EXTRACTOR = os.getenv("ENABLE_LOCAL_EXTRACTOR", "true").lower() == "true"

# Models that support thinking_budget=0 to disable internal chain-of-thought.
# gemini-3.5-flash-lite does NOT support thinking config — it raises 400 INVALID_ARGUMENT.
_THINKING_SUPPRESSED_MODELS = {"gemini-3.5-flash", "gemini-3.6-flash"}


PROMPT = """You read a shopkeeper's spoken or typed note about a customer's account.
The language may be Tamil, Tanglish (Tamil written in English letters) or English.
Return only JSON that matches the schema.

Rules:
- kind:
  * "credit" when only goods/items were taken on credit.
  * "payment" when only money/cash was paid back by the customer.
  * "combined" when the note mentions BOTH a repayment AND a new credit purchase in the same interaction (e.g. customer paid some money and also took groceries on credit).
- operations:
  * For "combined": provide each financial operation in order:
    1. type: "payment" with total_rupees set to repayment amount, and items empty.
    2. type: "credit" with total_rupees set to new credit purchase amount, and items set to products taken.
  * For "credit" or "payment": operations can contain that single operation.
- customer_name: the customer's name, written in English letters. Empty string if none was said.
- items: each product with quantity and unit (kg, g, L, ml, packet, piece). Use English product names
  (paruppu = Dal, arisi = Rice, paal = Milk, sakkarai = Sugar, ennai = Oil).
  Never fabricate item details if the merchant only stated a purchase amount.
- price_rupees: ONLY if a price for that single item was spoken, otherwise null. Never guess prices.
- total_rupees: the total amount spoken, as a number. null if no total was spoken. Never add up guessed prices.
  For "combined", this can be null or the new credit purchase amount.
- transcript: a short plain transcript of what was said.
- confidence: "high" if every field is clear, "medium" if something is uncertain (such as ambiguous payment vs credit direction), "low" if the audio or sentence was unclear.
"""


class Item(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    price_rupees: Optional[float] = None


class Operation(BaseModel):
    type: Literal["payment", "credit"]
    items: list[Item] = []
    total_rupees: Optional[float] = None


class Draft(BaseModel):
    kind: Literal["credit", "payment", "combined"] = "credit"
    customer_name: str = ""
    items: list[Item] = []
    total_rupees: Optional[float] = None
    operations: list[Operation] = []
    transcript: str = ""
    confidence: Literal["high", "medium", "low"] = "high"


class DraftResponse(Draft):
    metrics: Optional[dict] = None


class TextIn(BaseModel):
    text: str


app = FastAPI(title="CredYazh AI service")

_cached_client = None


def _client():
    global _cached_client
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise HTTPException(503, "GEMINI_API_KEY is not set in ai-service/.env")
    if _cached_client is None:
        from google import genai
        _cached_client = genai.Client(api_key=key)
    return _cached_client


def _new_request_id() -> str:
    return uuid.uuid4().hex[:12]


def _request_id_from(request: Request | None) -> str:
    if request is None:
        return _new_request_id()
    return (request.headers.get("x-request-id") or "").strip() or _new_request_id()


def _build_config(model_name: str, timeout_ms: int, extra_kwargs: dict | None = None) -> types.GenerateContentConfig:
    """Build a GenerateContentConfig with consistent defaults.

    Key choices:
    - temperature=0  : deterministic extraction, no creative variation.
    - thinking_budget=0 : disables chain-of-thought on supported models (saves 400–600 ms).
      gemini-3.5-flash-lite does NOT support ThinkingConfig and raises 400;
      we skip it for that model.
    - timeout : per-attempt cap that cannot exceed the remaining shared deadline.
    - max_output_tokens : keep structured drafts small.
    """
    kwargs: dict = dict(
        system_instruction=PROMPT,
        response_mime_type="application/json",
        response_schema=Draft,
        temperature=0,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        http_options=types.HttpOptions(
            timeout=int(timeout_ms),
            # Explicitly disable SDK retries (default is already 1 attempt when
            # retry_options is omitted; set attempts=1 so a 429/503 cannot stack
            # extra waits on top of the shared deadline).
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )
    if model_name in _THINKING_SUPPRESSED_MODELS:
        # thinking_budget=0 disables chain-of-thought tokens entirely on supported models.
        kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    return types.GenerateContentConfig(**kwargs)


def _strip_fences(raw_output: str) -> str:
    text = (raw_output or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def _ask(
    contents,
    model_list: list[str] | None = None,
    request_id: str | None = None,
    extra_metrics: dict | None = None,
    deadline_ms: int | None = None,
) -> DraftResponse:
    """Extract a draft with a bounded shared deadline across sequential model attempts.

    Individual attempt timeouts cannot exceed remaining budget. A new fallback is
    not started when insufficient time remains. Timed-out SDK calls use HttpOptions
    timeout so the transport can cancel the outstanding request.
    """
    client = _client()
    t_start = time.perf_counter()
    request_id = request_id or _new_request_id()
    models_attempted = []
    last_err = None
    last_err_class = None
    target_models = model_list or MODELS
    budget_ms = int(deadline_ms if deadline_ms is not None else SHARED_DEADLINE_MS)
    retry_wait_total_ms = 0.0
    fallback_request_ms = 0.0
    parsing_validation_ms = 0.0
    primary_latency_ms = 0.0
    skipped_for_deadline = False

    for attempt_number, model_name in enumerate(target_models, start=1):
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        timeout_ms = attempt_timeout_ms(budget_ms, elapsed_ms, REQUEST_TIMEOUT_MS, MIN_ATTEMPT_BUDGET_MS)
        if timeout_ms <= 0 or not should_start_attempt(budget_ms, elapsed_ms, MIN_ATTEMPT_BUDGET_MS):
            skipped_for_deadline = True
            logger.info(
                "ai_attempt request_id=%s skip_fallback remaining_ms=%s min_budget_ms=%s",
                request_id,
                remaining_ms(budget_ms, elapsed_ms),
                MIN_ATTEMPT_BUDGET_MS,
            )
            break

        t_model_start = time.perf_counter()
        timed_out = False
        try:
            logger.info(
                "ai_attempt request_id=%s model=%s attempt=%s timeout_ms=%s start",
                request_id, model_name, attempt_number, timeout_ms,
            )
            resp = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=_build_config(model_name, timeout_ms),
            )
            t_gen = (time.perf_counter() - t_model_start) * 1000
            if attempt_number == 1:
                primary_latency_ms = t_gen
            else:
                fallback_request_ms += t_gen

            raw_output = _strip_fences(resp.text or "")

            t_val_start = time.perf_counter()
            try:
                validated = Draft.model_validate_json(raw_output)
            except ValidationError as ve:
                t_val = (time.perf_counter() - t_val_start) * 1000
                parsing_validation_ms += t_val
                error_class = "malformed"
                models_attempted.append({
                    "model": model_name,
                    "attempt": attempt_number,
                    "latency_ms": round(t_gen, 1),
                    "status": error_class,
                    "timeout": False,
                    "http_status": None,
                    "error": "malformed_json",
                })
                logger.warning(
                    "ai_attempt request_id=%s model=%s attempt=%s duration_ms=%.0f status=%s timeout=false success=false",
                    request_id, model_name, attempt_number, t_gen, error_class,
                )
                last_err = ve
                last_err_class = error_class
                if not should_fallback(error_class):
                    break
                continue
            t_val = (time.perf_counter() - t_val_start) * 1000
            parsing_validation_ms += t_val
            t_total = (time.perf_counter() - t_start) * 1000

            usage = getattr(resp, "usage_metadata", None)
            models_attempted.append({
                "model": model_name,
                "attempt": attempt_number,
                "latency_ms": round(t_gen, 1),
                "status": "ok",
                "timeout": False,
                "prompt_tokens": getattr(usage, "prompt_token_count", None),
                "candidate_tokens": getattr(usage, "candidates_token_count", None),
                "thought_tokens": getattr(usage, "thoughts_token_count", None),
            })
            logger.info(
                "ai_attempt request_id=%s model=%s attempt=%s duration_ms=%.0f status=ok timeout=false success=true total_ms=%.0f",
                request_id, model_name, attempt_number, t_gen, t_total,
            )

            metrics = {
                "request_id": request_id,
                "model": model_name,
                "gemini_latency_ms": round(primary_latency_ms or t_gen, 1),
                "gemini_request_ms": round(primary_latency_ms or t_gen, 1),
                "fallback_request_ms": round(fallback_request_ms, 1),
                "retry_wait_ms": round(retry_wait_total_ms, 1),
                "parsing_validation_ms": round(parsing_validation_ms, 1),
                "validation_latency_ms": round(t_val, 1),
                "ai_total_latency_ms": round(t_total, 1),
                "ai_service_total_ms": round(t_total, 1),
                "deadline_ms": budget_ms,
                "models_attempted": models_attempted,
            }
            if extra_metrics:
                metrics.update(extra_metrics)
            return DraftResponse(**validated.model_dump(), metrics=metrics)
        except HTTPException:
            raise
        except Exception as e:
            dt = (time.perf_counter() - t_model_start) * 1000
            if attempt_number == 1:
                primary_latency_ms = dt
            else:
                fallback_request_ms += dt
            err_str = str(e)
            error_class = classify_error(err_str)
            timed_out = error_class == "timeout"
            last_err = e
            last_err_class = error_class

            logger.warning(
                "ai_attempt request_id=%s model=%s attempt=%s duration_ms=%.0f status=%s timeout=%s success=false",
                request_id, model_name, attempt_number, dt, error_class, str(timed_out).lower(),
            )
            models_attempted.append({
                "model": model_name,
                "attempt": attempt_number,
                "latency_ms": round(dt, 1),
                "status": error_class,
                "timeout": timed_out,
                "error": err_str[:200],
            })

            if error_class == "auth":
                raise HTTPException(503, "Gemini API authentication failed")

            if not should_fallback(error_class):
                break

            if error_class == "rate_limit":
                leftover = remaining_ms(budget_ms, (time.perf_counter() - t_start) * 1000)
                wait_ms = rate_limit_backoff_ms(leftover, RATE_LIMIT_BACKOFF_MS, MIN_ATTEMPT_BUDGET_MS)
                if wait_ms > 0:
                    time.sleep(wait_ms / 1000.0)
                    retry_wait_total_ms += wait_ms
            continue

    tried_summary = ", ".join(f"{m['model']} ({m['status']})" for m in models_attempted)
    reason = "DEADLINE_EXCEEDED" if skipped_for_deadline else f"All configured models failed: [{tried_summary}]"
    logger.warning(
        "ai_attempt request_id=%s all_failed reason=%s last_class=%s last_error=%s",
        request_id, reason, last_err_class, str(last_err)[:200] if last_err else "",
    )
    t_fallback_total = (time.perf_counter() - t_start) * 1000

    trace_parts = []
    for m in models_attempted:
        mod_name = m.get("model", "gemini")
        st = m.get("status", "err")
        err = str(m.get("error", ""))
        if "503" in err or "UNAVAILABLE" in err:
            code = "503"
        elif m.get("timeout") or "504" in err or "timeout" in err.lower() or "deadline" in err.lower() or st in ("transient", "timeout"):
            code = "timeout"
        elif st == "rate_limit":
            code = "429"
        else:
            code = st
        trace_parts.append(f"{mod_name}: {code}")
    if skipped_for_deadline:
        trace_parts.append("deadline_exhausted")
    trace_parts.append("Manual fallback")
    failover_trace = " -> ".join(trace_parts)

    metrics = {
        "request_id": request_id,
        "model": "manual_fallback",
        "provider": "manual_fallback",
        "gemini_latency_ms": round(primary_latency_ms, 1),
        "gemini_request_ms": round(primary_latency_ms, 1),
        "fallback_request_ms": round(fallback_request_ms, 1),
        "retry_wait_ms": round(retry_wait_total_ms, 1),
        "parsing_validation_ms": round(parsing_validation_ms, 1),
        "validation_latency_ms": 0.0,
        "ai_total_latency_ms": round(t_fallback_total, 1),
        "ai_service_total_ms": round(t_fallback_total, 1),
        "deadline_ms": budget_ms,
        "models_attempted": models_attempted,
        "failover_trace": failover_trace,
        "fallback_reason": reason,
        "deadline_exhausted": skipped_for_deadline,
    }
    if extra_metrics:
        metrics.update(extra_metrics)

    return DraftResponse(
        kind="credit",
        customer_name="",
        items=[],
        total_rupees=None,
        operations=[],
        transcript="",
        confidence="low",
        metrics=metrics,
    )


_orchestrator = None


def _get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        from failover_orchestrator import FailoverOrchestrator
        _orchestrator = FailoverOrchestrator()
    return _orchestrator


def _health_payload() -> dict:
    data = {
        "ok": True,
        "service": "credyazh-ai",
        "primary_model": MODELS[0] if MODELS else None,
        "configured_models": MODELS,
        "total_models": len(MODELS),
        "shared_deadline_ms": SHARED_DEADLINE_MS,
        "per_attempt_timeout_ms": REQUEST_TIMEOUT_MS,
        "min_attempt_budget_ms": MIN_ATTEMPT_BUDGET_MS,
        "failover_enabled": os.getenv("AI_FAILOVER_ENABLED", "false").lower() in ("true", "1", "yes"),
    }
    if data["failover_enabled"]:
        data["failover_status"] = _get_orchestrator().get_health_status()
    return data


@app.get("/")
def root():
    """Browsers open http://127.0.0.1:8000/ — do not 404; point at health and docs."""
    payload = _health_payload()
    payload["docs"] = "/docs"
    payload["health"] = "/health"
    return payload


@app.get("/health")
def health():
    return _health_payload()


@app.get("/json/version")
def json_version():
    """Chrome / IDE automation probes /json/version (CDP). This process is FastAPI, not Chrome."""
    return {
        "ok": True,
        "service": "credyazh-ai",
        "chrome_devtools": False,
        "health": "/health",
    }


@app.post("/draft/text", response_model=DraftResponse)
def draft_text(body: TextIn, request: Request):
    request_id = _request_id_from(request)
    if os.getenv("AI_FAILOVER_ENABLED", "false").lower() in ("true", "1", "yes"):
        return _get_orchestrator().extract_text(body.text, request_id=request_id)

    if ENABLE_LOCAL_EXTRACTOR:
        try:
            from credyazh_local_extractor import try_local_extract
            t0 = time.perf_counter()
            local_draft = try_local_extract(body.text)
            if local_draft is not None:
                dt_ms = (time.perf_counter() - t0) * 1000
                logger.info("local_fastpath request_id=%s duration_ms=%.2f", request_id, dt_ms)
                local_draft.pop("_source", None)
                validated = Draft.model_validate(local_draft)
                return DraftResponse(
                    **validated.model_dump(),
                    metrics={
                        "request_id": request_id,
                        "model": "local_regex_fastpath",
                        "gemini_latency_ms": 0.0,
                        "gemini_request_ms": 0.0,
                        "validation_latency_ms": round(dt_ms, 2),
                        "parsing_validation_ms": round(dt_ms, 2),
                        "ai_total_latency_ms": round(dt_ms, 2),
                        "ai_service_total_ms": round(dt_ms, 2),
                        "models_attempted": [{
                            "model": "local_regex_fastpath",
                            "latency_ms": round(dt_ms, 2),
                            "status": "ok"
                        }]
                    }
                )
        except Exception as e:
            logger.warning(f"Local extraction error: {e}, falling through to Gemini")
    return _ask([body.text], request_id=request_id)


@app.post("/draft/audio", response_model=DraftResponse)
async def draft_audio(request: Request):
    from google.genai import types
    data = None
    mime = "audio/wav"
    request_id = _request_id_from(request)
    t_decode = time.perf_counter()
    decode_path = "unknown"

    content_type = request.headers.get("content-type", "").lower()

    # 1. Handle JSON with base64 audio (legacy / serverless)
    if "application/json" in content_type:
        try:
            body = await request.json()
            b64_str = body.get("audio_base64") or body.get("audio") or ""
            if not b64_str:
                raise HTTPException(400, "empty audio_base64 in JSON payload")
            data = base64.b64decode(b64_str)
            mime = body.get("mime_type") or body.get("mimetype") or "audio/wav"
            decode_path = "json_base64"
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(400, f"Invalid base64 audio payload: {e}")

    # 2. Handle raw binary audio (preferred Node-to-Python path)
    elif "audio/" in content_type or "application/octet-stream" in content_type:
        data = await request.body()
        mime = content_type.split(";")[0] or "audio/wav"
        decode_path = "binary"

    # 3. Handle multipart form-data (with safe exception handling)
    else:
        try:
            form = await request.form()
            file = form.get("audio")
            if file and hasattr(file, "read"):
                data = await file.read()
                mime = getattr(file, "content_type", None) or "audio/wav"
                decode_path = "multipart"
            elif file and isinstance(file, (bytes, bytearray)):
                data = file
                decode_path = "multipart"
        except Exception as e:
            logger.warning(f"Multipart parse error: {e}. Trying raw body fallback.")
            raw = await request.body()
            if raw:
                data = raw
                mime = "audio/wav"
                decode_path = "raw_body"

    audio_decode_ms = (time.perf_counter() - t_decode) * 1000
    extra = {
        "request_id": request_id,
        "audio_decode_ms": round(audio_decode_ms, 1),
        "audio_bytes": len(data) if data else 0,
        "audio_decode_path": decode_path,
    }

    if not data:
        raise HTTPException(400, "Empty audio data received")

    logger.info(
        "audio_decode request_id=%s path=%s bytes=%s decode_ms=%.1f",
        request_id, decode_path, extra["audio_bytes"], audio_decode_ms,
    )

    # Route through the failover orchestrator when enabled so the shared
    # Gemini deadline is enforced and Groq Whisper failover is triggered.
    if os.getenv("AI_FAILOVER_ENABLED", "false").lower() in ("true", "1", "yes"):
        return _get_orchestrator().extract_audio(data, mime, request_id=request_id, extra_metrics=extra)

    # ── Phase 3: local fast-path on audio transcript ──────────────────────────
    # Gemini must first transcribe the audio to get a transcript string.
    # We send a lightweight text-only prompt to get just the transcript, then
    # run the local extractor. If it matches, we skip full JSON extraction entirely.
    # If not, we fall through to the normal full Gemini extraction below.
    if ENABLE_LOCAL_EXTRACTOR:
        try:
            from credyazh_local_extractor import try_local_extract
            # Ask Gemini for a plain transcript only (cheap, fast, no schema)
            t0_stt = time.perf_counter()
            stt_resp = _client().models.generate_content(
                model=MODELS[0],
                contents=[
                    types.Part.from_bytes(data=data, mime_type=mime),
                    "Transcribe exactly what was said. Return only the spoken words, nothing else.",
                ],
                config=types.GenerateContentConfig(
                    temperature=0,
                    max_output_tokens=128,
                    http_options=types.HttpOptions(
                        timeout=int(REQUEST_TIMEOUT_MS),
                        retry_options=types.HttpRetryOptions(attempts=1),
                    ),
                ),
            )
            stt_ms = (time.perf_counter() - t0_stt) * 1000
            transcript_text = (stt_resp.text or "").strip()
            if transcript_text:
                t0_local = time.perf_counter()
                local_draft = try_local_extract(transcript_text)
                local_ms = (time.perf_counter() - t0_local) * 1000
                if local_draft is not None:
                    logger.info(
                        "audio_local_fastpath request_id=%s stt_ms=%.1f local_ms=%.2f transcript=%r",
                        request_id, stt_ms, local_ms, transcript_text,
                    )
                    local_draft.pop("_source", None)
                    validated = Draft.model_validate(local_draft)
                    total_ms = stt_ms + local_ms
                    extra.update({
                        "stt_latency_ms": round(stt_ms, 1),
                        "local_extract_ms": round(local_ms, 2),
                        "transcript_text": transcript_text,
                    })
                    return DraftResponse(
                        **validated.model_dump(),
                        metrics={
                            "request_id": request_id,
                            "model": f"stt:{MODELS[0]}+local_regex",
                            "gemini_latency_ms": round(stt_ms, 1),
                            "gemini_request_ms": round(stt_ms, 1),
                            "fallback_request_ms": 0.0,
                            "retry_wait_ms": 0.0,
                            "parsing_validation_ms": round(local_ms, 2),
                            "validation_latency_ms": round(local_ms, 2),
                            "ai_total_latency_ms": round(total_ms, 1),
                            "ai_service_total_ms": round(total_ms, 1),
                            "deadline_ms": SHARED_DEADLINE_MS,
                            "models_attempted": [{
                                "model": f"stt:{MODELS[0]}+local_regex",
                                "latency_ms": round(total_ms, 1),
                                "status": "ok",
                            }],
                            **extra,
                        },
                    )
                logger.info(
                    "audio_local_fastpath_miss request_id=%s transcript=%r falling_to_gemini",
                    request_id, transcript_text,
                )
        except Exception as e:
            logger.warning("audio_local_fastpath error request_id=%s err=%s — falling to Gemini", request_id, e)

    # Keep configured model order (lite first on the free tier). Do not spend a
    # full independent timeout on a slower fallback before the primary returns.
    return _ask(
        [types.Part.from_bytes(data=data, mime_type=mime), "Read this note."],
        model_list=MODELS,
        request_id=request_id,
        extra_metrics=extra,
    )


# ─── WhatsApp message generation ─────────────────────────────
class TransactionLine(BaseModel):
    date: str
    type: Literal["credit", "payment", "reversal"]
    description: str
    amount_rupees: float


class WhatsAppMessageRequest(BaseModel):
    shop_name: str
    customer_name: str
    balance_rupees: float
    total_credit_rupees: float
    total_payment_rupees: float
    recent_transactions: list[TransactionLine]
    language: Literal["english", "tamil", "tanglish"] = "english"


class WhatsAppMessageResponse(BaseModel):
    message: str
    language: str


WA_PROMPT_TEMPLATE = """You are a polite customer relationship assistant for an Indian grocery shop called "{shop_name}".

Write a friendly WhatsApp account statement message to the customer named "{customer_name}" in {language_instruction}.

Rules:
- Be warm, respectful, and professional.
- Include the shop name as the sender.
- Show the current outstanding balance prominently.
- Summarize recent transactions clearly (credit vs repayment).
- Do NOT fabricate any numbers — use only the data provided.
- End with a polite thank you and invitation to contact if there are any discrepancies.
- Keep the message concise but complete (under 300 words).
- Use ₹ for amounts. Format amounts as ₹X,XXX (e.g. ₹1,250).
- Do not use any markdown formatting — plain text only, suitable for WhatsApp.
- {language_extra}

Account data:
Customer: {customer_name}
Outstanding Balance: ₹{balance_rupees:.2f}
Total Credit Given (all time): ₹{total_credit_rupees:.2f}
Total Repayments (all time): ₹{total_payment_rupees:.2f}

Recent Transactions:
{transaction_lines}

Return ONLY the WhatsApp message text, nothing else.
"""

LANGUAGE_INSTRUCTIONS = {
    "english": ("English", "Use formal but friendly English."),
    "tamil": ("Tamil (தமிழ்)", "Write in Tamil script. Use respectful language (நீங்கள் / உங்கள்)."),
    "tanglish": ("Tanglish (Tamil written in English letters)", "Write in Tanglish — Tamil words written using English alphabet. E.g. 'Vanakkam Kumar, ungal account pathi oru update...'"),
}


@app.post("/whatsapp-message", response_model=WhatsAppMessageResponse)
def generate_whatsapp_message(body: WhatsAppMessageRequest):
    lang_label, lang_extra = LANGUAGE_INSTRUCTIONS.get(body.language, LANGUAGE_INSTRUCTIONS["english"])

    tx_lines = "\n".join(
        f"  - {t.date}: {t.description} ({t.type.capitalize()}) ₹{t.amount_rupees:.2f}"
        for t in body.recent_transactions
    ) or "  (No transactions recorded yet)"

    prompt = WA_PROMPT_TEMPLATE.format(
        shop_name=body.shop_name,
        customer_name=body.customer_name,
        language_instruction=lang_label,
        language_extra=lang_extra,
        balance_rupees=body.balance_rupees,
        total_credit_rupees=body.total_credit_rupees,
        total_payment_rupees=body.total_payment_rupees,
        transaction_lines=tx_lines,
    )

    from google import genai
    from google.genai import types

    try:
        client = _client()
        for model_name in MODELS:
            try:
                logger.info(f"Generating WhatsApp message with model '{model_name}'")
                resp = client.models.generate_content(
                    model=model_name,
                    contents=[prompt],
                    config=types.GenerateContentConfig(temperature=0.4),
                )
                return WhatsAppMessageResponse(message=resp.text.strip(), language=body.language)
            except HTTPException:
                raise
            except Exception as e:
                logger.warning(f"WhatsApp message generation failed with '{model_name}': {e}")
                continue
    except HTTPException:
        raise
    except Exception:
        pass

    # Reliable template fallback (never fabricates data)
    if body.language == "tanglish":
        fallback = (
            f"Vanakkam {body.customer_name},\n\n"
            f"{body.shop_name} irundhu ungal account pathi oru update:\n\n"
            f"Current balance: \u20b9{body.balance_rupees:,.2f}\n"
            f"Total credit: \u20b9{body.total_credit_rupees:,.2f}\n"
            f"Total repayments: \u20b9{body.total_payment_rupees:,.2f}\n\n"
            f"Ungal support-ku nandri. Enna thappu irundhaal, engalai contact pannungal.\n\n"
            f"Regards,\n{body.shop_name}"
        )
    elif body.language == "tamil":
        fallback = (
            f"வணக்கம் {body.customer_name},\n\n"
            f"{body.shop_name} இல் இருந்து உங்கள் கணக்கு விவரம்:\n\n"
            f"நிலுவை தொகை: \u20b9{body.balance_rupees:,.2f}\n"
            f"மொத்த கடன்: \u20b9{body.total_credit_rupees:,.2f}\n"
            f"மொத்த திருப்பிச் செலுத்தியது: \u20b9{body.total_payment_rupees:,.2f}\n\n"
            f"உங்கள் ஆதரவிற்கு நன்றி. ஏதேனும் வேறுபாடு இருந்தால் எங்களை தொடர்பு கொள்ளுங்கள்.\n\n"
            f"நன்றி,\n{body.shop_name}"
        )
    else:
        fallback = (
            f"Hello {body.customer_name},\n\n"
            f"Greetings from {body.shop_name}!\n\n"
            f"Here is a friendly update on your account:\n\n"
            f"Outstanding Balance: \u20b9{body.balance_rupees:,.2f}\n"
            f"Total Credit Given: \u20b9{body.total_credit_rupees:,.2f}\n"
            f"Total Repayments: \u20b9{body.total_payment_rupees:,.2f}\n\n"
            f"Thank you for your continued support. Please contact us if you notice any discrepancy.\n\n"
            f"Regards,\n{body.shop_name}"
        )

    return WhatsAppMessageResponse(message=fallback, language=body.language)

