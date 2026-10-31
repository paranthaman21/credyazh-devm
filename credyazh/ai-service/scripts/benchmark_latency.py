"""Repeatable latency comparison for the bounded-deadline policy.

This script is SIMULATED by default (no live Gemini quota). It contrasts:

  * legacy sequential timeouts (10s + 10s)
  * current shared deadline (8s total, 6.5s per attempt, no Gemini retry on timeout)

Live API measurements require WAV files and GEMINI_API_KEY; they are opt-in:

  python scripts/benchmark_latency.py --live path/to/clip.wav
"""
from __future__ import annotations

import argparse
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gemini_deadline import attempt_timeout_ms, should_fallback, should_start_attempt


def percentile(values, p):
    if not values:
        return None
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, int(round((p / 100) * (len(ordered) - 1)))))
    return ordered[idx]


def simulate_legacy(primary_ms: float, fallback_ms: float, primary_ok: bool) -> float:
    """Independent 10s timeouts per model (the 21s incident shape)."""
    waited = min(primary_ms, 10000)
    if primary_ok and primary_ms <= 10000:
        return waited
    waited += min(fallback_ms, 10000)
    return waited


def simulate_bounded(primary_ms: float, fallback_ms: float, primary_error: str, deadline_ms=8000, cap_ms=6500, min_ms=2000) -> float:
    elapsed = 0.0
    timeout = attempt_timeout_ms(deadline_ms, elapsed, cap_ms, min_ms)
    waited = min(primary_ms, timeout)
    elapsed += waited
    if primary_error == "ok" and primary_ms <= timeout:
        return elapsed
    if not should_fallback(primary_error):
        return elapsed
    if not should_start_attempt(deadline_ms, elapsed, min_ms):
        return elapsed
    timeout2 = attempt_timeout_ms(deadline_ms, elapsed, cap_ms, min_ms)
    elapsed += min(fallback_ms, timeout2)
    return elapsed


SCENARIOS = [
    ("warm_success", 1800, 4000, "ok", True),
    ("slow_success", 5200, 4000, "ok", True),
    ("primary_timeout", 20000, 20000, "timeout", False),
    ("fast_503_then_ok", 250, 900, "transient", False),
]


def run_simulated(repeats: int) -> None:
    print("SIMULATED results (not live Gemini). Repeats per scenario:", repeats)
    print(f"{'scenario':<22} {'policy':<10} {'p50':>8} {'p90':>8} {'p95':>8} {'max':>8}")
    for name, primary, fallback, err, ok in SCENARIOS:
        legacy = [simulate_legacy(primary, fallback, ok) for _ in range(repeats)]
        bounded = [simulate_bounded(primary, fallback, err) for _ in range(repeats)]
        for label, samples in (("legacy", legacy), ("bounded", bounded)):
            print(
                f"{name:<22} {label:<10} "
                f"{percentile(samples, 50):8.0f} {percentile(samples, 90):8.0f} "
                f"{percentile(samples, 95):8.0f} {max(samples):8.0f}"
            )


def run_live(wav_path: str, repeats: int) -> None:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    import main
    from google.genai import types

    data = Path(wav_path).read_bytes()
    mime = "audio/wav"
    samples = []
    print(f"LIVE Gemini runs against {wav_path} (repeats={repeats}). Consumes quota.")
    for i in range(repeats):
        t0 = time.perf_counter()
        out = main._ask(
            [types.Part.from_bytes(data=data, mime_type=mime), "Read this note."],
            request_id=f"bench-{i}",
        )
        dt = (time.perf_counter() - t0) * 1000
        samples.append(dt)
        model = (out.metrics or {}).get("model")
        print(f"  run {i + 1}: {dt:.0f}ms model={model} gemini={(out.metrics or {}).get('gemini_request_ms')}")
    print(
        f"LIVE e2e-ai p50={percentile(samples, 50):.0f} p90={percentile(samples, 90):.0f} "
        f"p95={percentile(samples, 95):.0f} max={max(samples):.0f}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", metavar="WAV")
    parser.add_argument("--repeats", type=int, default=20)
    args = parser.parse_args()
    run_simulated(args.repeats)
    if args.live:
        run_live(args.live, min(args.repeats, 5))


if __name__ == "__main__":
    main()
