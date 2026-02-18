from __future__ import annotations

from pathlib import Path

from autopom.extraction.schema import PageModel


class ReportWriter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.report_dir = output_dir / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def write_summary(self, pages: list[PageModel]) -> Path:
        total_elements = sum(
            len(section.elements) for p in pages for section in p.sections
        )
        avg_confidence = (
            sum(e.confidence for p in pages for s in p.sections for e in s.elements)
            / total_elements
            if total_elements
            else 0.0
        )
        lines = [
            "# AutoPOM Crawl Report",
            "",
            f"- Pages modeled: {len(pages)}",
            f"- Elements mapped: {total_elements}",
            f"- Average selector confidence: {avg_confidence:.2f}",
        ]
        target = self.report_dir / "crawl_summary.md"
        target.write_text("\n".join(lines), encoding="utf-8")
        return target
