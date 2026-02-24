import unittest
from unittest.mock import MagicMock, patch
from autopom.browser.browseruse_adapter import (
    PlaywrightBrowserAdapter,
    create_browser_adapter,
)


class TestPlaywrightCDPConnection(unittest.TestCase):
    @patch("playwright.sync_api.sync_playwright")
    def test_connect_over_cdp_called(self, mock_sync_playwright):
        # Setup mocks
        mock_playwright_instance = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_playwright_instance
        mock_browser = MagicMock()
        mock_playwright_instance.chromium.connect_over_cdp.return_value = mock_browser

        # Mock contexts and pages
        mock_context = MagicMock()
        mock_browser.contexts = [mock_context]
        mock_page = MagicMock()
        mock_context.pages = [mock_page]
        mock_page.url = "http://existing-session.com"

        # Initialize adapter with cdp_url
        cdp_url = "http://localhost:9222"
        adapter = PlaywrightBrowserAdapter(base_url="http://dummy", cdp_url=cdp_url)

        # Verify connect_over_cdp was called
        mock_playwright_instance.chromium.connect_over_cdp.assert_called_once_with(
            cdp_url
        )
        mock_playwright_instance.chromium.launch.assert_not_called()

        # Verify it reused the page
        self.assertEqual(adapter._page, mock_page)
        self.assertEqual(adapter.url(), "http://existing-session.com")

    @patch("playwright.sync_api.sync_playwright")
    def test_connect_over_cdp_no_context(self, mock_sync_playwright):
        # Setup mocks
        mock_playwright_instance = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_playwright_instance
        mock_browser = MagicMock()
        mock_playwright_instance.chromium.connect_over_cdp.return_value = mock_browser

        # No contexts
        mock_browser.contexts = []
        mock_new_context = MagicMock()
        mock_new_context.pages = []
        mock_browser.new_context.return_value = mock_new_context
        mock_new_page = MagicMock()
        mock_new_context.new_page.return_value = mock_new_page
        mock_new_page.url = "about:blank"

        # Initialize adapter
        cdp_url = "http://localhost:9222"
        adapter = PlaywrightBrowserAdapter(
            base_url="http://fallback.com", cdp_url=cdp_url
        )

        # Verify new context and page created
        mock_browser.new_context.assert_called_once()
        mock_new_context.new_page.assert_called_once()
        self.assertEqual(adapter._page, mock_new_page)
        # Verify fallback URL is used if page is empty (though implementation uses page.url if not empty/about:blank)
        # In this mock, page.url is about:blank, so adapter._current_url should be base_url
        self.assertEqual(adapter.url(), "http://fallback.com")

    @patch("playwright.sync_api.sync_playwright")
    def test_create_browser_adapter_with_cdp(self, mock_sync_playwright):
        # Just verify the factory passes the argument
        mock_playwright_instance = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_playwright_instance
        mock_browser = MagicMock()
        mock_playwright_instance.chromium.connect_over_cdp.return_value = mock_browser
        mock_browser.contexts = []
        mock_browser.new_context.return_value.new_page.return_value = MagicMock()

        adapter = create_browser_adapter(
            adapter_name="playwright",
            base_url="http://test.com",
            cdp_url="http://localhost:1234",
        )

        self.assertIsInstance(adapter, PlaywrightBrowserAdapter)
        self.assertEqual(adapter.cdp_url, "http://localhost:1234")
        mock_playwright_instance.chromium.connect_over_cdp.assert_called_with(
            "http://localhost:1234"
        )


if __name__ == "__main__":
    unittest.main()
