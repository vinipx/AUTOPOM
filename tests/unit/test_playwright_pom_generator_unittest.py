from pathlib import Path
import tempfile
import unittest

from autopom.config import CrawlConfig
from autopom.extraction.schema import ActionModel, ElementModel, PageModel, SectionModel
from autopom.generation.java_generator import PlaywrightPomGenerator


def _sample_page() -> PageModel:
    return PageModel(
        page_id="login",
        page_name="LoginPage",
        url="https://example.com/login",
        route="/login",
        sections=[
            SectionModel(
                name="mainContent",
                elements=[
                    ElementModel(
                        element_id="usernameInput",
                        type="input",
                        role="textbox",
                        semantic_label="Username",
                        selector="input[name='username']",
                    ),
                    ElementModel(
                        element_id="signInButton",
                        type="button",
                        role="button",
                        semantic_label="Sign In",
                        selector='button:has-text("Sign In")',
                    ),
                ],
            )
        ],
        actions=[
            ActionModel(
                name="login",
                params=["username"],
                steps=["fill(usernameInput, username)", "click(signInButton)"],
            )
        ],
    )


class TestPlaywrightPomGenerator(unittest.TestCase):
    def test_generates_javascript_files_when_language_is_javascript(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            generator = PlaywrightPomGenerator(
                output_dir=output_dir,
                language="javascript",
                template_dir=Path("unused"),
            )

            base_path = generator.generate_base_page()
            page_path = generator.generate_page(_sample_page())

            self.assertEqual(
                base_path, output_dir / "javascript" / "base" / "BasePage.js"
            )
            self.assertEqual(
                page_path, output_dir / "javascript" / "pages" / "LoginPage.js"
            )

            page_content = page_path.read_text(encoding="utf-8")
            self.assertIn("class LoginPage extends BasePage", page_content)
            self.assertIn("async login(username)", page_content)
            self.assertIn("await this.signInButton.click()", page_content)

    def test_generates_typescript_files_when_language_is_typescript(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            generator = PlaywrightPomGenerator(
                output_dir=output_dir,
                language="typescript",
                template_dir=Path("unused"),
            )

            base_path = generator.generate_base_page()
            page_path = generator.generate_page(_sample_page())

            self.assertEqual(
                base_path, output_dir / "typescript" / "base" / "BasePage.ts"
            )
            self.assertEqual(
                page_path, output_dir / "typescript" / "pages" / "LoginPage.ts"
            )

            page_content = page_path.read_text(encoding="utf-8")
            self.assertIn(
                'import { Locator, Page } from "@playwright/test";', page_content
            )
            self.assertIn(
                "async login(username: string): Promise<LoginPage>", page_content
            )
            self.assertIn("await this.signInButton.click()", page_content)

    def test_crawl_config_normalizes_language_aliases(self) -> None:
        cfg = CrawlConfig(base_url="https://example.com", pom_language="ts")
        self.assertEqual(cfg.pom_language, "typescript")

        cfg_js = CrawlConfig(base_url="https://example.com", pom_language="js")
        self.assertEqual(cfg_js.pom_language, "javascript")

    def test_invalid_pom_language_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            CrawlConfig(base_url="https://example.com", pom_language="ruby")


if __name__ == "__main__":
    unittest.main()
