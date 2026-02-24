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


import os
import platform

def get_chrome_profile_path() -> str:
    system = platform.system()
    if system == "Darwin":
        return os.path.expanduser("~/Library/Application Support/Google/Chrome")
    elif system == "Windows":
        return os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    else: # Linux
        return os.path.expanduser("~/.config/google-chrome")

@dataclass(slots=True)
class PlaywrightBrowserAdapter:
    """Live browser adapter backed by Playwright (sync API)."""

    base_url: str
    headless: bool = True
    cdp_url: str | None = None
    chrome_profile: bool = False
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

        if self.cdp_url:
            print(f"Connecting to existing browser at {self.cdp_url}...")
            self._browser = self._playwright.chromium.connect_over_cdp(self.cdp_url)
            # Use existing context if available, else create new
            if self._browser.contexts:
                self._context = self._browser.contexts[0]
            else:
                self._context = self._browser.new_context()
            
            # Use existing page if available
            if self._context.pages:
                self._page = self._context.pages[-1]
                self._page.bring_to_front()
            else:
                self._page = self._context.new_page()
            
            self._current_url = self._page.url
            if not self._current_url or self._current_url == "about:blank":
                 self._current_url = self.base_url

        elif self.chrome_profile:
            profile_path = get_chrome_profile_path()
            print(f"Launching with local Chrome profile at {profile_path}...")
            try:
                self._context = self._playwright.chromium.launch_persistent_context(
                    user_data_dir=profile_path,
                    headless=self.headless,
                    # Usually we want a non-headless browser to debug if we use profile
                    channel="chrome", # requires actual Chrome installed
                )
                self._browser = self._context.browser # might be None in persistent context
                if self._context.pages:
                    self._page = self._context.pages[-1]
                    self._page.bring_to_front()
                else:
                    self._page = self._context.new_page()
                    
                self._current_url = self._page.url
                if not self._current_url or self._current_url == "about:blank":
                     self._current_url = self.base_url
            except Exception as e:
                if "locked" in str(e).lower() or "singletonlock" in str(e).lower():
                    raise RuntimeError("Chrome profile is locked. Please completely close all existing Google Chrome windows (you can run `killall \"Google Chrome\"` in your terminal) before running with the Chrome Profile option.") from e
                raise e
        else:
            self._browser = self._playwright.chromium.launch(headless=self.headless)
            self._context = self._browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720},
                locale="en-US",
            )
            self._page = self._context.new_page()
            self._current_url = self.base_url

        self._page.set_default_timeout(self.navigation_timeout_ms)

    def goto(self, url: str) -> None:
        if self.cdp_url:
            # If connected to existing browser, we might not want to navigate if we're already there.
            # But the orchestrator might call goto.
            # If the URL is the same, just reload or do nothing?
            # For now, we follow standard behavior.
            pass
        
        try:
            self._page.goto(
                url, wait_until="domcontentloaded", timeout=self.navigation_timeout_ms
            )
        except Exception:
            # If navigation times out, we assume the page is at least partially loaded and proceed.
            pass

        self._page.wait_for_timeout(1000)
        self._current_url = self._page.url

    def url(self) -> str:
        page_url = self._page.url
        if not page_url or page_url == "about:blank":
            return self._current_url or self.base_url
        return page_url

    def title(self) -> str:
        return self._page.title()

    def extract_interactive_dom_summary(self, max_nodes: int = 500) -> dict:
        try:
            # Use functional map/filter approach which proved drastically faster than imperative loops
            result = self._page.evaluate(
                """
                ({ maxNodes }) => {
                    // Helper to clean text
                    const cleanText = (txt) => (txt || '').replace(/\\s+/g, ' ').trim();
                    const escapeSelector = (val) => val.replace(/"/g, '\\\\"');

                    // 1. Process Interactive Elements (High Priority)
                    // Expanded selector for comprehensive coverage
                    const interactiveSelector = `
                        input:not([type="hidden"]), select, textarea, button,
                        [role="button"], [role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"],
                        [role="checkbox"], [role="radio"], [role="switch"],
                        [role="tab"], [role="combobox"], [role="listbox"], [role="option"],
                        [role="searchbox"], [role="spinbutton"], [role="slider"],
                        [contenteditable="true"], [tabindex]:not([tabindex="-1"])
                    `;
                    
                    const formElements = Array.from(document.querySelectorAll(interactiveSelector))
                        .slice(0, 500)
                        .map(el => {
                            const tag = el.tagName.toLowerCase();
                            const roleAttr = el.getAttribute('role');
                            let role = roleAttr || 'generic';
                            
                            // Refined role detection
                            if (tag === 'input' || tag === 'textarea' || tag === 'select') role = 'textbox';
                            if (tag === 'button') role = 'button';
                            if (el.getAttribute('contenteditable') === 'true') role = 'textbox';
                            
                            // Label extraction hierarchy
                            let label = el.name || el.id || el.value || el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.title;
                            if (role === 'button' || role === 'link' || role === 'menuitem' || !label) {
                                label = cleanText(el.innerText || el.textContent) || label;
                            }
                            label = (label || role).slice(0, 80);

                            // Robust Selector Construction
                            let selector = tag;
                            const id = el.id;
                            const name = el.name;
                            const testId = el.getAttribute('data-testid') || el.getAttribute('data-test');
                            const placeholder = el.getAttribute('placeholder');
                            const ariaLabel = el.getAttribute('aria-label');
                            const title = el.title;

                            if (testId) selector += `[data-testid="${escapeSelector(testId)}"]`;
                            else if (id) selector = `#${id}`; // IDs are strong
                            else if (name) selector += `[name="${escapeSelector(name)}"]`;
                            else if (placeholder) selector += `[placeholder="${escapeSelector(placeholder)}"]`;
                            else if (ariaLabel) selector += `[aria-label="${escapeSelector(ariaLabel)}"]`;
                            else if (title) selector += `[title="${escapeSelector(title)}"]`;
                            else if ((role === 'button' || role === 'link' || role === 'menuitem') && label) selector += `:has-text("${escapeSelector(label)}")`;
                            else if (roleAttr) selector += `[role="${roleAttr}"]`;
                            
                            // Class fallback
                            if (selector === tag && el.className && typeof el.className === 'string') {
                                selector += `.${el.className.split(' ').filter(c => c).join('.')}`;
                            }

                            const safeLabel = label.replace(/\\|/g, '');
                            return `${role}|${safeLabel}|${selector}|main`;
                        })
                        .filter(Boolean);

                    // 2. Process Links (Navigation Coverage)
                    const linkElements = Array.from(document.links)
                        .slice(0, 300)
                        .map(link => {
                            const href = link.href;
                            if (!href || href.startsWith('javascript:') || href.includes('#')) return null;
                            
                            const text = cleanText(link.textContent);
                            const label = text.slice(0, 80) || 'link';
                            const selector = `a[href="${escapeSelector(href)}"]`;
                            
                            const safeLabel = label.replace(/\\|/g, '');
                            return `link|${safeLabel}|${selector}|main`;
                        })
                        .filter(Boolean);

                    // Combine: Interactive elements first, then Links
                    const allElements = formElements.concat(linkElements);
                    
                    // Deduplicate strings directly
                    const uniqueElements = Array.from(new Set(allElements)).slice(0, maxNodes);

                    // Extract frontier links
                    const frontierLinks = Array.from(document.links)
                        .slice(0, 300)
                        .map(a => a.href)
                        .filter(h => h && !h.startsWith('javascript:'));

                    return {
                        fingerprint: `fast::${document.title}::${uniqueElements.length}`,
                        landmarks: ['main'],
                        elements: uniqueElements,
                        links: frontierLinks
                    };
                }
                """,
                {"maxNodes": max_nodes},
            )

            # Parse the string elements back into dicts in Python
            parsed_elements = []
            raw_elements = result.get("elements", [])

            for item in raw_elements:
                parts = item.split("|")
                # Handle cases where label/selector might have pipes or fewer parts
                if len(parts) >= 2:
                    role = parts[0]
                    label = parts[1]
                    # Join the rest as selector+section
                    rest = "|".join(parts[2:])
                    # Assume last part is section, everything before is selector
                    if "|" in rest:
                        selector, section = rest.rsplit("|", 1)
                    else:
                        selector = rest
                        section = "main"

                    parsed_elements.append(
                        {
                            "role": role,
                            "label": label,
                            "selector": selector,
                            "section": section,
                        }
                    )

            result["elements"] = parsed_elements
            return result

        except Exception:
            # Fallback empty result
            return {
                "fingerprint": "error",
                "landmarks": [],
                "elements": [],
                "links": [],
            }

    def capture_screenshot(self, scale: float = 0.4) -> str | None:
        # Screenshot not yet persisted in this scaffold implementation.
        return None

    def is_visible(self, selector: str, timeout_ms: int = 1500) -> bool:
        if not selector:
            return False
        try:
            # Check immediate visibility without waiting, avoiding timeouts on hidden elements
            return self._page.locator(selector).first.is_visible()
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
    adapter_name: str,
    base_url: str,
    playwright_headless: bool = True,
    cdp_url: str | None = None,
    chrome_profile: bool = False,
) -> BrowserAdapter:
    normalized = normalize_browser_adapter(adapter_name)
    if normalized == "playwright":
        return PlaywrightBrowserAdapter(
            base_url=base_url,
            headless=playwright_headless,
            cdp_url=cdp_url,
            chrome_profile=chrome_profile,
        )
    return MockBrowserUseAdapter(base_url=base_url)
