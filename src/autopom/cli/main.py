from __future__ import annotations

import argparse
from pathlib import Path

from autopom.agent.orchestrator import AutoPomOrchestrator
from autopom.browser.browseruse_adapter import MockBrowserUseAdapter
from autopom.config import CrawlConfig
from autopom.generation.java_generator import SUPPORTED_POM_LANGUAGES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AutoPOM-Agent CLI")
    parser.add_argument("--base-url", required=True, help="Base URL to crawl")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    parser.add_argument("--max-depth", type=int, default=3, help="Max link depth")
    parser.add_argument("--max-pages", type=int, default=20, help="Max pages to model")
    parser.add_argument(
        "--pom-language",
        default="java",
        choices=SUPPORTED_POM_LANGUAGES,
        help="POM language: java, javascript, or typescript",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = CrawlConfig(
        base_url=args.base_url,
        output_dir=Path(args.output_dir),
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        pom_language=args.pom_language,
    )
    browser = MockBrowserUseAdapter(base_url=args.base_url)
    orchestrator = AutoPomOrchestrator(config=config, browser=browser)
    result = orchestrator.run()

    print(f"Modeled pages: {len(result.pages)}")
    print(f"Saved models: {len(result.model_paths)}")
    print(f"Generated Java files: {len(result.java_paths)}")
    print(f"Report: {result.report_path}")


if __name__ == "__main__":
    main()
