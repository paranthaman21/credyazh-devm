"""Shared deadline / timeout utilities for CredYazh AI service.

Used by both main.py (direct Gemini path) and failover_orchestrator.py
(multi-provider path).  Keeping these in one place ensures consistent
error classification and budget arithmetic across both code-paths.
"""

import os
from typing import Optional

# ── Default constants (overridden via .env / environment variables) ───────────
DEFAULT_SHARED_DEADLINE_MS: int = 8000
DEFAULT_PER_ATTEMPT_TIMEOUT_MS: int = 6500
DEFAULT_MIN_ATTEMPT_BUDGET_MS: int = 2000

# ── Error patterns ─────────────────────────────────────────────────────────────
_TIMEOUT_MARKERS = (
    "deadline exceeded",
    "timeout",
    "timed out",
    "504",
    "read timeout",
    "connect timeout",
    "DeadlineExceeded",
    "DEADLINE_EXCEEDED",
)
_RATE_LIMIT_MARKERS = ("429", "resource_exhausted", "RESOURCE_EXHAUSTED", "rate limit", "quota")
_TRANSIENT_MARKERS = ("503", "UNAVAILABLE", "unavailable", "500", "internal", "502", "bad gateway")
_AUTH_MARKERS = ("401", "403", "UNAUTHENTICATED", "PERMISSION_DENIED", "api key", "invalid api key")

# Error classes that warrant trying the next model / provider.
_FALLBACK_ELIGIBLE = {"timeout", "rate_limit", "transient"}


def env_int(name: str, default: int) -> int:
    """Read an integer from the environment, falling back to *default*."""
    raw = os.getenv(name, "")
    try:
        return int(raw) if raw.strip() else default
    except ValueError:
        return default


def classify_error(err_str: str) -> str:
    """Map a raw exception string to a canonical error class.

    Returns one of: ``"timeout"``, ``"rate_limit"``, ``"transient"``,
    ``"auth"``, or ``"unknown"``.
    """
    lower = err_str.lower()
    if any(m.lower() in lower for m in _TIMEOUT_MARKERS):
        return "timeout"
    if any(m.lower() in lower for m in _RATE_LIMIT_MARKERS):
        return "rate_limit"
    if any(m.lower() in lower for m in _AUTH_MARKERS):
        return "auth"
    if any(m.lower() in lower for m in _TRANSIENT_MARKERS):
        return "transient"
    return "unknown"


def should_fallback(error_class: str) -> bool:
    """Return True if we should try the next model/provider for this error class."""
    return error_class in _FALLBACK_ELIGIBLE


def remaining_ms(budget_ms: int, elapsed_ms: float) -> float:
    """How many milliseconds are left in the shared deadline budget."""
    return max(0.0, budget_ms - elapsed_ms)


def should_start_attempt(budget_ms: int, elapsed_ms: float, min_budget_ms: int) -> bool:
    """Return True if enough budget remains to warrant starting another attempt."""
    return remaining_ms(budget_ms, elapsed_ms) >= min_budget_ms


def attempt_timeout_ms(
    budget_ms: int,
    elapsed_ms: float,
    per_attempt_cap_ms: int,
    min_budget_ms: int,
) -> int:
    """Compute the timeout for the current attempt.

    The value is the *minimum* of the configured per-attempt cap and the
    remaining shared deadline, clamped to zero when below *min_budget_ms*.
    """
    left = remaining_ms(budget_ms, elapsed_ms)
    if left < min_budget_ms:
        return 0
    return int(min(per_attempt_cap_ms, left))


def rate_limit_backoff_ms(
    remaining_budget_ms: float,
    configured_backoff_ms: int,
    min_attempt_budget_ms: int,
) -> int:
    """Return how long to wait after a 429 rate-limit response.

    Returns 0 if the budget is too tight to afford a wait.
    """
    # Keep enough budget for at least one more attempt after the wait.
    max_wait = remaining_budget_ms - min_attempt_budget_ms
    if max_wait <= 0:
        return 0
    return int(min(configured_backoff_ms, max_wait))

