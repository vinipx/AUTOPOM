# Changelog

## 0.3.0

- Added live `playwright` browser adapter with CLI/config selection.
- Added enterprise-grade `run.sh` guided wizard with transparent dependency setup.
- Added optimized dependency/runtime checks to skip unnecessary reinstall work.
- Added live execution progress logs (`[CRAWL]`, `[MAP]`, `[SKIP]`).
- Added run-end managerial summaries:
  - `reports/execution_summary.md`
  - `reports/execution_summary.json`

## 0.2.0

- Added configurable multi-language Playwright POM generation (`java`, `javascript`, `typescript`).
- Added `pom_language` support in CLI and `CrawlConfig`.
- Added language-aware output directories (`output/<language>`).
- Added unit and integration coverage for language selection, alias normalization, and invalid language validation.
- Updated docs and site content to reflect architecture and configuration changes.

## 0.1.0

- Initial AutoPOM-Agent implementation scaffold.
- Added crawler orchestration and state management.
- Added selector verification and healing flow.
- Added Java POM generation pipeline.
- Added Docusaurus documentation site with architecture, guides, tutorials, and use cases.
