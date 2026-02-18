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

## `BrowserAdapter`

Runtime browser abstraction for navigation and extraction.

Methods:

- `goto(url)`
- `url()`
- `title()`
- `extract_interactive_dom_summary(max_nodes=120)`
- `capture_screenshot(scale=0.4)`
- `is_visible(selector, timeout_ms=1500)`

## `PageModel`

Intermediate structured representation used for generation.

Includes:

- page identity and route metadata
- sectioned element mappings
- inferred actions
- discovered links
- navigation hints
