from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from autopom.browser.browseruse_adapter import normalize_browser_adapter
from autopom.generation.java_generator import normalize_pom_language


@dataclass(slots=True)
class CrawlConfig:
    base_url: str
    output_dir: Path = Path("output")
    max_depth: int = 3
    max_pages: int = 80
    max_actions_per_page: int = 12
    same_origin_only: bool = True
    denied_domains: list[str] = field(
        default_factory=lambda: ["facebook.com", "twitter.com", "linkedin.com"]
    )
    preferred_testid_attrs: list[str] = field(
        default_factory=lambda: ["data-testid", "data-test", "data-qa"]
    )
    auth_user_env: str = "AUTOPOM_USERNAME"
    auth_pass_env: str = "AUTOPOM_PASSWORD"
    pom_language: str = "java"
    browser_adapter: str = "mock"
    playwright_headless: bool = True

    def __post_init__(self) -> None:
        self.pom_language = normalize_pom_language(self.pom_language)
        self.browser_adapter = normalize_browser_adapter(self.browser_adapter)
