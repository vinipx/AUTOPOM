import unittest

from autopom.extraction.schema import ElementModel, PageModel, SectionModel
from autopom.healing.selector_verifier import SelectorVerifier


class FakeVisibilityBrowser:
    def __init__(self, visible_selectors: set[str]) -> None:
        self.visible_selectors = visible_selectors

    def is_visible(self, selector: str, timeout_ms: int = 1500) -> bool:
        return selector in self.visible_selectors


class TestSelectorVerifier(unittest.TestCase):
    def _build_page(self, selector: str, fallbacks: list[str], confidence: float = 0.8) -> PageModel:
        element = ElementModel(
            element_id="exampleButton",
            type="button",
            role="button",
            semantic_label="Example",
            selector=selector,
            fallback_selectors=fallbacks,
            confidence=confidence,
            section="mainContent",
        )
        return PageModel(
            page_id="example",
            page_name="ExamplePage",
            url="https://example.com/example",
            route="/example",
            sections=[SectionModel(name="mainContent", elements=[element])],
        )

    def test_keeps_primary_selector_when_visible(self) -> None:
        page = self._build_page("button.primary", ["text=Example"])
        verifier = SelectorVerifier(FakeVisibilityBrowser({"button.primary"}))

        verifier.verify_and_heal(page)

        element = page.sections[0].elements[0]
        self.assertEqual(element.selector, "button.primary")
        self.assertAlmostEqual(element.confidence, 0.85, places=6)

    def test_promotes_first_visible_fallback(self) -> None:
        page = self._build_page("button.missing", ["text=Example", "[data-testid='example']"])
        verifier = SelectorVerifier(FakeVisibilityBrowser({"[data-testid='example']"}))

        verifier.verify_and_heal(page)

        element = page.sections[0].elements[0]
        self.assertEqual(element.selector, "[data-testid='example']")
        self.assertAlmostEqual(element.confidence, 0.82, places=6)

    def test_decreases_confidence_when_no_selector_is_visible(self) -> None:
        page = self._build_page("button.missing", ["text=Example"], confidence=0.4)
        verifier = SelectorVerifier(FakeVisibilityBrowser(set()))

        verifier.verify_and_heal(page)

        element = page.sections[0].elements[0]
        self.assertEqual(element.selector, "button.missing")
        self.assertEqual(element.confidence, 0.3)


if __name__ == "__main__":
    unittest.main()
