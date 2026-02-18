import json
from pathlib import Path
import tempfile
import unittest

from autopom.agent.orchestrator import AutoPomOrchestrator
from autopom.browser.browseruse_adapter import MockBrowserUseAdapter
from autopom.config import CrawlConfig


class TestOrchestratorIntegration(unittest.TestCase):
    def test_end_to_end_run_generates_expected_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            config = CrawlConfig(
                base_url="https://example.com",
                output_dir=output_dir,
                max_depth=2,
                max_pages=5,
            )
            orchestrator = AutoPomOrchestrator(
                config=config,
                browser=MockBrowserUseAdapter(base_url=config.base_url),
            )

            result = orchestrator.run()

            self.assertEqual(len(result.pages), 3)
            self.assertTrue(result.report_path.exists())
            self.assertTrue((output_dir / "java" / "base" / "BasePage.java").exists())
            self.assertTrue((output_dir / "java" / "pages" / "LoginPage.java").exists())
            self.assertTrue((output_dir / "models_json" / "LoginPage.json").exists())

            login_page_json = json.loads(
                (output_dir / "models_json" / "LoginPage.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(login_page_json["page_name"], "LoginPage")
            self.assertEqual(len(login_page_json["actions"]), 1)
            self.assertEqual(login_page_json["actions"][0]["name"], "login")

            report_content = result.report_path.read_text(encoding="utf-8")
            self.assertIn("Pages modeled: 3", report_content)
            self.assertIn("Elements mapped:", report_content)

    def test_same_origin_policy_blocks_external_links(self) -> None:
        class ExternalLinkBrowser(MockBrowserUseAdapter):
            def extract_interactive_dom_summary(self, max_nodes: int = 120) -> dict:
                summary = super().extract_interactive_dom_summary(max_nodes=max_nodes)
                summary["links"] = ["https://facebook.com/external-page"]
                return summary

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            config = CrawlConfig(
                base_url="https://example.com",
                output_dir=output_dir,
                max_depth=3,
                max_pages=10,
                same_origin_only=True,
            )
            orchestrator = AutoPomOrchestrator(
                config=config,
                browser=ExternalLinkBrowser(base_url=config.base_url),
            )

            result = orchestrator.run()

            # External links are ignored, so only the seed page should be modeled.
            self.assertEqual(len(result.pages), 1)
            self.assertEqual(result.pages[0].page_name, "HomePage")


if __name__ == "__main__":
    unittest.main()
