from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urljoin, urlparse


class BrowserAdapter(Protocol):
    def goto(self, url: str) -> None: ...
    def url(self) -> str: ...
    def title(self) -> str: ...
    def extract_interactive_dom_summary(self, max_nodes: int = 120) -> dict: ...
    def capture_screenshot(self, scale: float = 0.4) -> str | None: ...
    def is_visible(self, selector: str, timeout_ms: int = 1500) -> bool: ...


@dataclass(slots=True)
class MockBrowserUseAdapter:
    """Local, deterministic adapter for initial scaffolding and tests."""

    base_url: str
    _current_url: str = ""

    def goto(self, url: str) -> None:
        self._current_url = url

    def url(self) -> str:
        return self._current_url or self.base_url

    def title(self) -> str:
        path = urlparse(self.url()).path or "/"
        return f"Mock Page {path}"

    def extract_interactive_dom_summary(self, max_nodes: int = 120) -> dict:
        path = urlparse(self.url()).path
        if path == "/login":
            elements = [
                {
                    "role": "textbox",
                    "label": "Username",
                    "selector": "input[name='username']",
                },
                {
                    "role": "textbox",
                    "label": "Password",
                    "selector": "input[name='password']",
                },
                {
                    "role": "button",
                    "label": "Sign In",
                    "selector": "button:has-text('Sign In')",
                },
            ]
            links = [urljoin(self.base_url, "/forgot-password")]
        else:
            elements = [
                {"role": "link", "label": "Login", "selector": "a[href='/login']"},
            ]
            links = [urljoin(self.base_url, "/login")]

        return {
            "fingerprint": f"mock::{path}::{len(elements)}",
            "landmarks": ["main"],
            "elements": elements[:max_nodes],
            "links": links,
        }

    def capture_screenshot(self, scale: float = 0.4) -> str | None:
        return None

    def is_visible(self, selector: str, timeout_ms: int = 1500) -> bool:
        # Mock visibility assumes selectors extracted from summary are valid.
        return bool(selector)
