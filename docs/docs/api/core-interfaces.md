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

`pom_language` accepts:

- `java`
- `javascript` (alias: `js`)
- `typescript` (alias: `ts`)

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

## `CrawlResult`

Primary run result returned by orchestrator.

Includes:

- `pages: list[PageModel]`
- `model_paths: list[Path]`
- `pom_paths: list[Path]` (language-specific generated artifacts)
- `report_path: Path`

Compatibility helper:

- `java_paths` is preserved as an alias to `pom_paths` for existing integrations.
