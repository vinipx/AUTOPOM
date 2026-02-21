from __future__ import annotations

import argparse
import json
from pathlib import Path
import time
from datetime import datetime, timezone

from autopom.agent.orchestrator import AutoPomOrchestrator
from autopom.browser.browseruse_adapter import (
    SUPPORTED_BROWSER_ADAPTERS,
    create_browser_adapter,
)
from autopom.config import CrawlConfig
from autopom.generation.java_generator import (
    SUPPORTED_LOCATOR_STORAGE,
    SUPPORTED_POM_LANGUAGES,
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _write_execution_summary(
    config: CrawlConfig,
    duration_seconds: float,
    crawl_report_path: Path,
    pages: list,
    model_paths: list[Path],
    pom_paths: list[Path],
) -> tuple[Path, Path]:
    reports_dir = config.output_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    total_elements = sum(len(section.elements) for p in pages for section in p.sections)
    total_actions = sum(len(p.actions) for p in pages)
    confidence_values = [
        e.confidence for p in pages for s in p.sections for e in s.elements
    ]
    avg_confidence = (
        (sum(confidence_values) / len(confidence_values)) if confidence_values else 0.0
    )

    payload = {
        "generated_at_utc": _utc_now_iso(),
        "duration_seconds": round(duration_seconds, 2),
        "configuration": {
            "base_url": config.base_url,
            "output_dir": str(config.output_dir),
            "pom_language": config.pom_language,
            "locator_storage": config.locator_storage,
            "browser_adapter": config.browser_adapter,
            "playwright_headless": config.playwright_headless,
            "max_depth": config.max_depth,
            "max_pages": config.max_pages,
            "same_origin_only": config.same_origin_only,
        },
        "metrics": {
            "pages_modeled": len(pages),
            "elements_mapped": total_elements,
            "actions_inferred": total_actions,
            "avg_selector_confidence": round(avg_confidence, 3),
            "json_models_saved": len(model_paths),
            "pom_files_generated": len(pom_paths),
            "page_object_files_generated": max(0, len(pom_paths) - 1),
            "base_page_files_generated": 1 if pom_paths else 0,
        },
        "artifacts": {
            "crawl_summary_report": str(crawl_report_path),
            "json_model_paths": [str(p) for p in model_paths],
            "pom_paths": [str(p) for p in pom_paths],
        },
    }

    markdown_lines = [
        "# AUTOPOM Execution Summary",
        "",
        "## Configuration",
        "",
        f"- Base URL: `{payload['configuration']['base_url']}`",
        f"- Output directory: `{payload['configuration']['output_dir']}`",
        f"- POM language: `{payload['configuration']['pom_language']}`",
        f"- Locator storage: `{payload['configuration']['locator_storage']}`",
        f"- Browser adapter: `{payload['configuration']['browser_adapter']}`",
        f"- Playwright headless: `{payload['configuration']['playwright_headless']}`",
        f"- Max depth: `{payload['configuration']['max_depth']}`",
        f"- Max pages: `{payload['configuration']['max_pages']}`",
        f"- Same-origin only: `{payload['configuration']['same_origin_only']}`",
        "",
        "## Metrics",
        "",
        f"- Duration (seconds): `{payload['duration_seconds']}`",
        f"- Pages modeled: `{payload['metrics']['pages_modeled']}`",
        f"- Elements mapped: `{payload['metrics']['elements_mapped']}`",
        f"- Actions inferred: `{payload['metrics']['actions_inferred']}`",
        f"- Average selector confidence: `{payload['metrics']['avg_selector_confidence']}`",
        f"- JSON models saved: `{payload['metrics']['json_models_saved']}`",
        f"- POM files generated: `{payload['metrics']['pom_files_generated']}`",
        "",
        "## Outputs",
        "",
        f"- Crawl summary report: `{payload['artifacts']['crawl_summary_report']}`",
        f"- JSON models directory: `{config.output_dir / 'models_json'}`",
        f"- POM output directory: `{config.output_dir / config.pom_language}`",
        "",
        "## Generated At",
        "",
        f"- UTC timestamp: `{payload['generated_at_utc']}`",
    ]

    markdown_path = reports_dir / "execution_summary.md"
    json_path = reports_dir / "execution_summary.json"
    markdown_path.write_text("\n".join(markdown_lines), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return markdown_path, json_path


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
    parser.add_argument(
        "--locator-storage",
        default="inline",
        choices=SUPPORTED_LOCATOR_STORAGE,
        help="Locator storage: inline or external",
    )
    parser.add_argument(
        "--browser-adapter",
        default="mock",
        choices=SUPPORTED_BROWSER_ADAPTERS,
        help="Browser adapter: mock or playwright",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run Playwright with visible browser window",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started_at = time.perf_counter()
    config = CrawlConfig(
        base_url=args.base_url,
        output_dir=Path(args.output_dir),
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        pom_language=args.pom_language,
        locator_storage=args.locator_storage,
        browser_adapter=args.browser_adapter,
        playwright_headless=not args.headed,
    )

    def progress_printer(event: str, payload: dict) -> None:
        if event == "dequeue":
            print(
                "[CRAWL] Visiting "
                f"{payload['url']} | depth={payload['depth']} "
                f"| modeled={payload['modeled_pages']} "
                f"| queue={payload['frontier_remaining']}"
            )
        elif event == "modeled":
            print(
                "[MAP] "
                f"{payload['page_name']} "
                f"| elements={payload['elements']} "
                f"| actions={payload['actions']} "
                f"| total_modeled={payload['modeled_pages']}"
            )
        elif event == "skip":
            reason = payload.get("reason", "unknown")
            print(f"[SKIP] {payload.get('url', '<unknown>')} | reason={reason}")

    browser = create_browser_adapter(
        adapter_name=config.browser_adapter,
        base_url=args.base_url,
        playwright_headless=config.playwright_headless,
    )
    try:
        orchestrator = AutoPomOrchestrator(
            config=config, browser=browser, progress_hook=progress_printer
        )
        result = orchestrator.run()
    finally:
        browser.close()
    duration_seconds = time.perf_counter() - started_at
    summary_md_path, summary_json_path = _write_execution_summary(
        config=config,
        duration_seconds=duration_seconds,
        crawl_report_path=result.report_path,
        pages=result.pages,
        model_paths=result.model_paths,
        pom_paths=result.pom_paths,
    )

    print(f"Modeled pages: {len(result.pages)}")
    print(f"Saved models: {len(result.model_paths)}")
    print(f"Generated POM files: {len(result.pom_paths)}")
    print(f"Crawl report: {result.report_path}")
    print(f"Execution summary (MD): {summary_md_path}")
    print(f"Execution summary (JSON): {summary_json_path}")
    print(f"Elapsed seconds: {duration_seconds:.2f}")


if __name__ == "__main__":
    main()
