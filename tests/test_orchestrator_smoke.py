from pathlib import Path

from autopom.agent.orchestrator import AutoPomOrchestrator
from autopom.browser.browseruse_adapter import MockBrowserUseAdapter
from autopom.config import CrawlConfig


def test_orchestrator_generates_outputs(tmp_path: Path) -> None:
    cfg = CrawlConfig(base_url="https://example.com", output_dir=tmp_path, max_depth=2, max_pages=5)
    browser = MockBrowserUseAdapter(base_url=cfg.base_url)
    orchestrator = AutoPomOrchestrator(config=cfg, browser=browser)

    result = orchestrator.run()

    assert result.pages
    assert result.model_paths
    assert result.java_paths
    assert result.report_path.exists()
