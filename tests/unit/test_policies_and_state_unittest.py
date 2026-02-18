import unittest

from autopom.agent.policies import is_denied_domain, normalize_url, same_origin
from autopom.agent.state_store import CrawlState


class TestPoliciesAndState(unittest.TestCase):
    def test_normalize_url_removes_fragment_and_tracking(self) -> None:
        url = "https://example.com/path?b=2&utm_source=x&a=1#section"
        normalized = normalize_url(url)
        self.assertEqual(normalized, "https://example.com/path?a=1&b=2")

    def test_same_origin_and_denied_domain(self) -> None:
        self.assertTrue(
            same_origin("https://app.example.com", "https://app.example.com/page")
        )
        self.assertFalse(
            same_origin("https://app.example.com", "https://other.example.com/page")
        )

        denied = ["facebook.com", "twitter.com"]
        self.assertTrue(is_denied_domain("https://m.facebook.com/foo", denied))
        self.assertFalse(is_denied_domain("https://app.example.com/foo", denied))

    def test_signature_is_deterministic(self) -> None:
        state = CrawlState()
        signature_a = state.make_signature(
            normalized_url="https://example.com/login",
            dom_fingerprint="fp-1",
            landmarks=["main", "nav"],
        )
        signature_b = state.make_signature(
            normalized_url="https://example.com/login",
            dom_fingerprint="fp-1",
            landmarks=["main", "nav"],
        )
        signature_c = state.make_signature(
            normalized_url="https://example.com/login",
            dom_fingerprint="fp-2",
            landmarks=["main", "nav"],
        )
        self.assertEqual(signature_a, signature_b)
        self.assertNotEqual(signature_a, signature_c)


if __name__ == "__main__":
    unittest.main()
