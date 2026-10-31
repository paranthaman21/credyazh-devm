"""Mocked Gemini tests for bounded-deadline extraction in main._ask."""
import json
import os
import unittest
from unittest.mock import MagicMock, patch

os.environ.setdefault("GEMINI_API_KEY", "mock_gemini_key_for_testing")
os.environ.setdefault("AI_FAILOVER_ENABLED", "false")

import main  # noqa: E402


VALID_CREDIT = json.dumps({
    "kind": "credit",
    "customer_name": "Barath",
    "items": [{"name": "Sugar", "quantity": 2.0, "unit": "kg", "price_rupees": None}],
    "total_rupees": 120.0,
    "operations": [],
    "transcript": "Barath 2 kg sakkarai 120 rupees",
    "confidence": "high",
})

VALID_COMBINED = json.dumps({
    "kind": "combined",
    "customer_name": "Kumar",
    "items": [{"name": "Rice", "quantity": 1.0, "unit": "kg", "price_rupees": None}],
    "total_rupees": 70.0,
    "operations": [
        {"type": "payment", "items": [], "total_rupees": 200.0},
        {"type": "credit", "items": [{"name": "Rice", "quantity": 1.0, "unit": "kg", "price_rupees": None}], "total_rupees": 70.0},
    ],
    "transcript": "Kumar 200 rupees kuduthutu 70 rupees-ku arisi",
    "confidence": "high",
})

MODELS = ["gemini-3.5-flash-lite", "gemini-3.5-flash"]


def _ok(text):
    resp = MagicMock()
    resp.text = text
    resp.usage_metadata = None
    return resp


class TestAskDeadline(unittest.TestCase):
    def _run(self, client, clock=None, **kwargs):
        patches = [
            patch.object(main, "_client", return_value=client),
            patch.object(main, "SHARED_DEADLINE_MS", 8000),
            patch.object(main, "REQUEST_TIMEOUT_MS", 6500),
            patch.object(main, "MIN_ATTEMPT_BUDGET_MS", 2000),
        ]
        if clock is not None:
            patches.append(patch("main.time.perf_counter", side_effect=clock))
        with patches[0], patches[1], patches[2], patches[3]:
            if clock is not None:
                with patches[4]:
                    return main._ask(["note"], model_list=MODELS, request_id="req-test", **kwargs)
            return main._ask(["note"], model_list=MODELS, request_id="req-test", **kwargs)

    def test_primary_success_does_not_call_fallback(self):
        client = MagicMock()
        client.models.generate_content.return_value = _ok(VALID_CREDIT)
        out = self._run(client)
        self.assertEqual(client.models.generate_content.call_count, 1)
        self.assertEqual(out.customer_name, "Barath")
        self.assertEqual(out.total_rupees, 120.0)
        self.assertEqual(out.items[0].price_rupees, None)
        self.assertEqual(out.metrics["models_attempted"][0]["status"], "ok")
        cfg = client.models.generate_content.call_args.kwargs["config"]
        self.assertLessEqual(cfg.http_options.timeout, 6500)
        self.assertEqual(cfg.http_options.retry_options.attempts, 1)

    def test_primary_timeout_does_not_start_second_gemini(self):
        client = MagicMock()
        client.models.generate_content.side_effect = Exception("The request timed out after 6500ms")
        out = self._run(client)
        self.assertEqual(client.models.generate_content.call_count, 1)
        self.assertEqual(out.metrics["model"], "manual_fallback")
        self.assertEqual(out.confidence, "low")
        self.assertTrue(out.metrics["models_attempted"][0]["timeout"])
        self.assertEqual(out.customer_name, "")
        self.assertIsNone(out.total_rupees)

    def test_fast_transient_falls_back_within_deadline(self):
        client = MagicMock()
        client.models.generate_content.side_effect = [
            Exception("503 UNAVAILABLE: The model is overloaded"),
            _ok(VALID_CREDIT),
        ]
        out = self._run(client)
        self.assertEqual(client.models.generate_content.call_count, 2)
        self.assertEqual(out.customer_name, "Barath")
        self.assertEqual(out.metrics["model"], "gemini-3.5-flash")
        self.assertGreater(out.metrics["fallback_request_ms"], 0)

    def test_no_fallback_when_deadline_exhausted_after_transient(self):
        client = MagicMock()
        state = {"t": 0.0}

        def perf():
            return state["t"]

        def generate(*_a, **_k):
            state["t"] += 6.6
            raise Exception("503 UNAVAILABLE")

        client.models.generate_content.side_effect = generate
        with patch.object(main, "_client", return_value=client), \
             patch.object(main, "SHARED_DEADLINE_MS", 8000), \
             patch.object(main, "REQUEST_TIMEOUT_MS", 6500), \
             patch.object(main, "MIN_ATTEMPT_BUDGET_MS", 2000), \
             patch("main.time.perf_counter", side_effect=perf):
            out = main._ask(["note"], model_list=MODELS, request_id="req-dl", deadline_ms=8000)
        self.assertEqual(client.models.generate_content.call_count, 1)
        self.assertTrue(out.metrics["deadline_exhausted"])
        self.assertEqual(out.metrics["model"], "manual_fallback")

    def test_invalid_request_is_not_retried(self):
        client = MagicMock()
        client.models.generate_content.side_effect = Exception("400 INVALID_ARGUMENT: unknown field")
        out = self._run(client)
        self.assertEqual(client.models.generate_content.call_count, 1)
        self.assertEqual(out.metrics["models_attempted"][0]["status"], "invalid_request")

    def test_malformed_json_may_try_next_model(self):
        client = MagicMock()
        bad = MagicMock()
        bad.text = "not-json {{"
        bad.usage_metadata = None
        client.models.generate_content.side_effect = [bad, _ok(VALID_CREDIT)]
        out = self._run(client)
        self.assertEqual(client.models.generate_content.call_count, 2)
        self.assertEqual(out.customer_name, "Barath")
        self.assertEqual(out.metrics["models_attempted"][0]["status"], "malformed")

    def test_rate_limit_uses_bounded_backoff_then_fallback(self):
        client = MagicMock()
        client.models.generate_content.side_effect = [
            Exception("429 RESOURCE_EXHAUSTED rate limit"),
            _ok(VALID_CREDIT),
        ]
        with patch("main.time.sleep") as sleep:
            out = self._run(client)
        self.assertEqual(client.models.generate_content.call_count, 2)
        self.assertTrue(sleep.called)
        self.assertEqual(out.customer_name, "Barath")
        self.assertGreaterEqual(out.metrics["retry_wait_ms"], 0)

    def test_combined_payment_and_credit_preserved(self):
        client = MagicMock()
        client.models.generate_content.return_value = _ok(VALID_COMBINED)
        out = self._run(client)
        self.assertEqual(out.kind, "combined")
        self.assertEqual(out.operations[0].type, "payment")
        self.assertEqual(out.operations[0].total_rupees, 200.0)
        self.assertEqual(out.operations[1].type, "credit")
        self.assertEqual(out.operations[1].total_rupees, 70.0)
        self.assertEqual(out.items[0].price_rupees, None)

    def test_auth_failure_raises_without_fallback(self):
        client = MagicMock()
        client.models.generate_content.side_effect = Exception("401 API_KEY_INVALID")
        from fastapi import HTTPException
        with self.assertRaises(HTTPException):
            self._run(client)
        self.assertEqual(client.models.generate_content.call_count, 1)


if __name__ == "__main__":
    unittest.main()
