import unittest

from autopom.browser.browseruse_adapter import (
    MockBrowserUseAdapter,
    create_browser_adapter,
    normalize_browser_adapter,
)
from autopom.cli.main import build_parser
from autopom.config import CrawlConfig


class TestCliAndBrowserAdapter(unittest.TestCase):
    def test_normalize_browser_adapter_alias_and_default(self) -> None:
        self.assertEqual(normalize_browser_adapter("mock"), "mock")
        self.assertEqual(normalize_browser_adapter("pw"), "playwright")

    def test_invalid_browser_adapter_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            normalize_browser_adapter("selenium")

    def test_create_browser_adapter_returns_mock_instance(self) -> None:
        adapter = create_browser_adapter("mock", "https://example.com")
        self.assertIsInstance(adapter, MockBrowserUseAdapter)
        adapter.close()

    def test_cli_parser_supports_browser_adapter_and_headed(self) -> None:
        parser = build_parser()
        args = parser.parse_args(
            [
                "--base-url",
                "https://example.com",
                "--browser-adapter",
                "playwright",
                "--headed",
            ]
        )
        self.assertEqual(args.browser_adapter, "playwright")
        self.assertTrue(args.headed)

    def test_crawl_config_normalizes_browser_adapter(self) -> None:
        cfg = CrawlConfig(base_url="https://example.com", browser_adapter="pw")
        self.assertEqual(cfg.browser_adapter, "playwright")


if __name__ == "__main__":
    unittest.main()
