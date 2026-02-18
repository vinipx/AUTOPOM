from __future__ import annotations

from autopom.browser.browseruse_adapter import BrowserAdapter
from autopom.extraction.schema import PageModel


class SelectorVerifier:
    def __init__(self, browser: BrowserAdapter) -> None:
        self.browser = browser

    def verify_and_heal(self, page_model: PageModel) -> None:
        for section in page_model.sections:
            for element in section.elements:
                if self.browser.is_visible(element.selector):
                    element.confidence = min(0.99, element.confidence + 0.05)
                    continue

                healed = False
                for candidate in element.fallback_selectors:
                    if self.browser.is_visible(candidate):
                        element.selector = candidate
                        element.confidence = min(0.95, element.confidence + 0.02)
                        healed = True
                        break

                if not healed:
                    element.confidence = max(0.3, element.confidence - 0.2)
