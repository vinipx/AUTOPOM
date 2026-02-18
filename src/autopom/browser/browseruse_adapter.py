from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from urllib.parse import urljoin, urlparse


class BrowserAdapter(Protocol):
    def goto(self, url: str) -> None: ...
    def url(self) -> str: ...
    def title(self) -> str: ...
    def extract_interactive_dom_summary(self, max_nodes: int = 120) -> dict: ...
    def capture_screenshot(self, scale: float = 0.4) -> str | None: ...
    def is_visible(self, selector: str, timeout_ms: int = 1500) -> bool: ...
    def close(self) -> None: ...


SUPPORTED_BROWSER_ADAPTERS = ("mock", "playwright")


def normalize_browser_adapter(adapter_name: str) -> str:
    normalized = adapter_name.strip().lower()
    aliases = {"pw": "playwright"}
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_BROWSER_ADAPTERS:
        allowed = ", ".join(SUPPORTED_BROWSER_ADAPTERS)
        raise ValueError(
            f"Unsupported browser adapter '{adapter_name}'. Allowed: {allowed}."
        )
    return normalized


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

    def close(self) -> None:
        return None


@dataclass(slots=True)
class PlaywrightBrowserAdapter:
    """Live browser adapter backed by Playwright (sync API)."""

    base_url: str
    headless: bool = True
    navigation_timeout_ms: int = 15000
    _sync_playwright: object = field(init=False, repr=False)
    _playwright: object = field(init=False, repr=False)
    _browser: object = field(init=False, repr=False)
    _context: object = field(init=False, repr=False)
    _page: object = field(init=False, repr=False)
    _current_url: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(
                "Playwright adapter selected, but Playwright is not installed. "
                "Install with: python -m pip install -e '.[browser]' "
                "and run: python -m playwright install chromium"
            ) from exc

        self._sync_playwright = sync_playwright
        self._playwright = self._sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        self._page.set_default_timeout(self.navigation_timeout_ms)
        self._current_url = self.base_url

    def goto(self, url: str) -> None:
        self._page.goto(
            url, wait_until="domcontentloaded", timeout=self.navigation_timeout_ms
        )
        self._current_url = self._page.url

    def url(self) -> str:
        return self._page.url or self._current_url or self.base_url

    def title(self) -> str:
        return self._page.title()

    def extract_interactive_dom_summary(self, max_nodes: int = 120) -> dict:
        result = self._page.evaluate(
            """
            ({ maxNodes }) => {
              const interactiveSelector =
                'a[href],button,input,select,textarea,[role="button"],[role="link"],[role="textbox"],[tabindex]';
              const nodes = Array.from(document.querySelectorAll(interactiveSelector));
              const safeAttr = (el, name) => (el.getAttribute(name) || '').trim();
              const toRole = (el) => {
                const role = safeAttr(el, 'role');
                if (role) return role.toLowerCase();
                const tag = el.tagName.toLowerCase();
                if (tag === 'a') return 'link';
                if (tag === 'button') return 'button';
                if (tag === 'input' || tag === 'textarea') return 'textbox';
                return 'generic';
              };
              const toLabel = (el) => {
                const fromAttrs = safeAttr(el, 'aria-label') || safeAttr(el, 'placeholder') || safeAttr(el, 'name');
                if (fromAttrs) return fromAttrs;
                const text = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                if (text) return text.slice(0, 80);
                return el.tagName.toLowerCase();
              };
              const cssEscape = (value) => {
                if (typeof CSS !== 'undefined' && typeof CSS.escape === 'function') {
                  return CSS.escape(value);
                }
                return value.replace(/([ #;?%&,.+*~\\':"!^$\\[\\]()=>|/@])/g, '\\\\$1');
              };
              const quoteAttr = (value) => value.replace(/"/g, '\\\\"');
              const toSelector = (el, role, label) => {
                const testAttrs = ['data-testid', 'data-test', 'data-qa'];
                for (const attr of testAttrs) {
                  const v = safeAttr(el, attr);
                  if (v) return `[${attr}="${quoteAttr(v)}"]`;
                }
                const id = safeAttr(el, 'id');
                if (id) return `#${cssEscape(id)}`;
                const tag = el.tagName.toLowerCase();
                const name = safeAttr(el, 'name');
                if (name && (tag === 'input' || tag === 'textarea' || tag === 'select')) {
                  return `${tag}[name="${quoteAttr(name)}"]`;
                }
                const href = safeAttr(el, 'href');
                if (tag === 'a' && href) {
                  return `a[href="${quoteAttr(href)}"]`;
                }
                if (label && (role === 'button' || role === 'link')) {
                  return `${role} >> text=${label}`;
                }
                return tag;
              };
              const sectionFor = (el) => {
                const landmark = el.closest('main,nav,header,footer,section,form,aside');
                if (!landmark) return 'mainContent';
                if (landmark.id) return landmark.id;
                const role = safeAttr(landmark, 'role');
                return role || landmark.tagName.toLowerCase() || 'mainContent';
              };

              const kept = [];
              for (const node of nodes) {
                if (kept.length >= maxNodes) break;
                const role = toRole(node);
                const label = toLabel(node);
                const selector = toSelector(node, role, label);
                kept.push({
                  role,
                  label,
                  selector,
                  section: sectionFor(node),
                });
              }

              const links = Array.from(
                new Set(
                  Array.from(document.querySelectorAll('a[href]'))
                    .map((a) => a.getAttribute('href'))
                    .filter(Boolean)
                )
              );

              const landmarks = Array.from(
                new Set(kept.map((k) => k.section).filter(Boolean))
              );
              const path = location.pathname || '/';
              const fingerprint = `live::${path}::${kept.length}::${links.length}`;
              return {
                fingerprint,
                landmarks: landmarks.length ? landmarks : ['mainContent'],
                elements: kept,
                links,
              };
            }
            """,
            {"maxNodes": max_nodes},
        )
        return result

    def capture_screenshot(self, scale: float = 0.4) -> str | None:
        # Screenshot not yet persisted in this scaffold implementation.
        return None

    def is_visible(self, selector: str, timeout_ms: int = 1500) -> bool:
        if not selector:
            return False
        try:
            locator = self._page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout_ms)
            return True
        except Exception:
            return False

    def close(self) -> None:
        try:
            self._context.close()
            self._browser.close()
            self._playwright.stop()
        except Exception:
            # Best effort teardown to avoid masking crawl results.
            return None


def create_browser_adapter(
    adapter_name: str, base_url: str, playwright_headless: bool = True
) -> BrowserAdapter:
    normalized = normalize_browser_adapter(adapter_name)
    if normalized == "playwright":
        return PlaywrightBrowserAdapter(
            base_url=base_url,
            headless=playwright_headless,
        )
    return MockBrowserUseAdapter(base_url=base_url)
