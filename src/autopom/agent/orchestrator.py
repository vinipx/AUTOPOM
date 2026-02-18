from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlparse

from autopom.agent.policies import is_denied_domain, normalize_url, same_origin
from autopom.agent.state_store import CrawlState, FrontierItem
from autopom.browser.browseruse_adapter import BrowserAdapter
from autopom.config import CrawlConfig
from autopom.extraction.schema import (
    ActionModel,
    ElementModel,
    PageModel,
    SectionModel,
)
from autopom.generation.java_generator import JavaGenerator, JavaGeneratorConfig
from autopom.healing.selector_verifier import SelectorVerifier
from autopom.io.persistence import Persistence
from autopom.io.report_writer import ReportWriter


@dataclass(slots=True)
class CrawlResult:
    pages: list[PageModel]
    model_paths: list[Path]
    java_paths: list[Path]
    report_path: Path


class AutoPomOrchestrator:
    def __init__(self, config: CrawlConfig, browser: BrowserAdapter) -> None:
        self.config = config
        self.browser = browser
        self.state = CrawlState()
        self.state.enqueue(FrontierItem(config.base_url, 0))

        self.persistence = Persistence(config.output_dir)
        self.reporter = ReportWriter(config.output_dir)
        template_dir = (
            Path(__file__).resolve().parents[1] / "generation" / "java_templates"
        )
        self.java_generator = JavaGenerator(
            output_dir=config.output_dir,
            template_dir=template_dir,
            config=JavaGeneratorConfig(),
        )
        self.verifier = SelectorVerifier(browser)

    def run(self) -> CrawlResult:
        pages: list[PageModel] = []
        model_paths: list[Path] = []
        java_paths: list[Path] = [self.java_generator.generate_base_page()]

        while self.state.frontier and self.state.page_count < self.config.max_pages:
            current = self.state.dequeue()
            if current is None:
                break
            if current.depth > self.config.max_depth:
                continue
            if not self._is_allowed(current.url):
                continue

            self.browser.goto(current.url)
            dom_summary = self.browser.extract_interactive_dom_summary(max_nodes=120)
            signature = self.state.make_signature(
                normalized_url=normalize_url(self.browser.url()),
                dom_fingerprint=dom_summary.get("fingerprint", ""),
                landmarks=dom_summary.get("landmarks", []),
            )
            if signature in self.state.visited_signatures:
                self.state.duplicate_hits += 1
                continue
            self.state.visited_signatures.add(signature)

            page_model = self._build_page_model(dom_summary)
            self.verifier.verify_and_heal(page_model)

            pages.append(page_model)
            model_paths.append(self.persistence.write_page_model(page_model))
            java_paths.append(self.java_generator.generate_page(page_model))

            self.state.page_count += 1
            self._enqueue_links(dom_summary.get("links", []), current.depth + 1)

        report_path = self.reporter.write_summary(pages)
        return CrawlResult(
            pages=pages,
            model_paths=model_paths,
            java_paths=java_paths,
            report_path=report_path,
        )

    def _build_page_model(self, dom_summary: dict) -> PageModel:
        url = self.browser.url()
        path = urlparse(url).path or "/"
        page_name = self._to_page_name(path)

        elements = []
        for e in dom_summary.get("elements", []):
            label = e.get("label", "Element")
            role = e.get("role", "generic")
            semantic_name = self._semantic_name_from_label(label, role)
            selector = e.get("selector", "")
            fallbacks = self._fallback_selectors(selector, label)
            el_type = (
                "button"
                if role == "button"
                else "input"
                if role == "textbox"
                else "link"
            )
            elements.append(
                ElementModel(
                    element_id=semantic_name,
                    type=el_type,
                    role=role,
                    semantic_label=label,
                    selector=selector,
                    fallback_selectors=fallbacks,
                    confidence=0.85,
                    section="mainContent",
                )
            )

        actions = self._infer_actions(path, elements)
        return PageModel(
            page_id=page_name.replace("Page", "").lower(),
            page_name=page_name,
            url=url,
            route=path,
            sections=[SectionModel(name="mainContent", elements=elements)],
            actions=actions,
            discovered_links=dom_summary.get("links", []),
            next_navigation_hints=[
                "Continue crawl for newly discovered same-origin pages."
            ],
        )

    @staticmethod
    def _to_page_name(path: str) -> str:
        if path in ("", "/"):
            return "HomePage"
        parts = [p for p in path.split("/") if p]
        return "".join(part.capitalize() for part in parts) + "Page"

    @staticmethod
    def _semantic_name_from_label(label: str, role: str) -> str:
        normalized = "".join(ch for ch in label.title() if ch.isalnum())
        suffix = (
            "Button" if role == "button" else "Input" if role == "textbox" else "Link"
        )
        if normalized.lower() in {"x", "close"}:
            normalized = "CloseModal"
            suffix = "Button"
        return normalized[:1].lower() + normalized[1:] + suffix

    @staticmethod
    def _fallback_selectors(selector: str, label: str) -> list[str]:
        fallbacks = []
        if label:
            fallbacks.append(f"text={label}")
        if selector and "data-testid" not in selector:
            fallbacks.append(f"[data-testid='{label.lower().replace(' ', '-')}']")
        return fallbacks

    @staticmethod
    def _infer_actions(path: str, elements: list[ElementModel]) -> list[ActionModel]:
        element_ids = {e.element_id for e in elements}
        if path == "/login" and {
            "usernameInput",
            "passwordInput",
            "signInButton",
        }.issubset(element_ids):
            return [
                ActionModel(
                    name="login",
                    params=["username", "password"],
                    steps=[
                        "fill(usernameInput, username)",
                        "fill(passwordInput, password)",
                        "click(signInButton)",
                    ],
                    post_condition="dashboardLoaded",
                )
            ]
        return []

    def _enqueue_links(self, links: list[str], depth: int) -> None:
        for link in links:
            absolute = urljoin(self.config.base_url, link)
            if not self._is_allowed(absolute):
                continue
            self.state.enqueue(
                FrontierItem(url=absolute, depth=depth, via_action="discover_link")
            )

    def _is_allowed(self, url: str) -> bool:
        if is_denied_domain(url, self.config.denied_domains):
            return False
        if self.config.same_origin_only and not same_origin(self.config.base_url, url):
            return False
        return True
