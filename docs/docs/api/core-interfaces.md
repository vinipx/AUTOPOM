# API Reference: Core Interfaces

## `CrawlConfig`

Controls crawl behavior and output policies.

Key fields:

- `base_url: str`
- `max_depth: int`
- `max_pages: int`
- `same_origin_only: bool`
- `denied_domains: list[str]`
- `output_dir: Path`
- `pom_language: str`
- `locator_storage: str` (`inline` or `external`)
- `browser_adapter: str`
- `playwright_headless: bool`
- `cdp_url: str | None`
- `chrome_profile: bool`
- `interactive_pause: bool`

## `BrowserAdapter`

Runtime browser abstraction for navigation and extraction.

Methods:

- `goto(url)`
- `url()`
- `title()`
- `extract_interactive_dom_summary(max_nodes=500)`
- `capture_screenshot(scale=0.4)`
- `is_visible(selector, timeout_ms=1500)`
- `close()`

### `PlaywrightBrowserAdapter` specifics

Supports advanced initialization:
- `cdp_url`: Connects to a running browser instance.
- `chrome_profile`: Launches with the default local Chrome profile.
- Headless/Headed toggle.

## Progress hook events

`AutoPomOrchestrator` supports a progress callback used by the CLI to stream runtime visibility.

Event types:

- `dequeue` - URL picked from frontier queue.
- `modeled` - page model generated and persisted.
- `skip` - URL ignored with a reason (policy, duplicate, depth).

## `PageModel`

Intermediate structured representation used for generation.

Includes:

- page identity and route metadata
- sectioned element mappings
- inferred actions
- discovered links
- navigation hints

## `CrawlResult`

Primary run result returned by orchestrator.

Includes:

- `pages: list[PageModel]`
- `model_paths: list[Path]`
- `pom_paths: list[Path]` (language-specific generated artifacts)
- `report_path: Path`

Compatibility helper:

- `java_paths` is preserved as an alias to `pom_paths` for existing integrations.

## Execution summary artifacts

CLI runs also emit:

- `reports/execution_summary.md` (manager-facing)
- `reports/execution_summary.json` (machine-facing)

These include effective configuration, elapsed time, counts for pages/elements/actions, and artifact paths.
