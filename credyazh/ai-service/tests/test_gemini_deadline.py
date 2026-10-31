"""Unit tests for shared AI deadline math and error classification."""
import unittest

from gemini_deadline import (
    attempt_timeout_ms,
    classify_error,
    remaining_ms,
    should_fallback,
    should_failover_provider,
    should_start_attempt,
    rate_limit_backoff_ms,
)


class TestDeadlineMath(unittest.TestCase):
    def test_attempt_timeout_capped_by_remaining_budget(self):
        self.assertEqual(attempt_timeout_ms(8000, 0, 6500, 2000), 6500)
        self.assertEqual(attempt_timeout_ms(8000, 3000, 6500, 2000), 5000)

    def test_no_attempt_when_budget_exhausted(self):
        self.assertEqual(attempt_timeout_ms(8000, 6500, 6500, 2000), 0)
        self.assertFalse(should_start_attempt(8000, 6500, 2000))
        self.assertEqual(remaining_ms(8000, 6500), 1500)

    def test_rate_limit_backoff_skipped_when_it_would_exhaust_budget(self):
        self.assertEqual(rate_limit_backoff_ms(2100, 250, 2000), 0)
        self.assertEqual(rate_limit_backoff_ms(4000, 250, 2000), 250)


class TestErrorPolicy(unittest.TestCase):
    def test_classify_distinct_classes(self):
        self.assertEqual(classify_error("504 Gateway Timeout: deadline exceeded"), "timeout")
        self.assertEqual(classify_error("HTTP 504"), "timeout")
        self.assertEqual(classify_error("503 UNAVAILABLE: overloaded"), "transient")
        self.assertEqual(classify_error("429 RESOURCE_EXHAUSTED rate limit"), "rate_limit")
        self.assertEqual(classify_error("400 INVALID_ARGUMENT"), "invalid_request")
        self.assertEqual(classify_error("API_KEY_INVALID 401"), "auth")
        self.assertEqual(classify_error("404 models/gemini-x is not found"), "not_found")

    def test_timeout_does_not_start_another_gemini_model(self):
        self.assertFalse(should_fallback("timeout"))
        self.assertFalse(should_fallback(classify_error("HTTP 504")))
        self.assertTrue(should_failover_provider("timeout"))

    def test_permanent_failures_do_not_retry(self):
        self.assertFalse(should_fallback("auth"))
        self.assertFalse(should_fallback("invalid_request"))
        self.assertFalse(should_failover_provider("auth"))
        self.assertFalse(should_failover_provider("invalid_request"))

    def test_transient_and_malformed_may_try_next_gemini(self):
        self.assertTrue(should_fallback("transient"))
        self.assertTrue(should_fallback("malformed"))
        self.assertTrue(should_fallback("not_found"))
        self.assertTrue(should_fallback("rate_limit"))


if __name__ == "__main__":
    unittest.main()
