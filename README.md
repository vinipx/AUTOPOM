<div align="center">

# AUTOPOM

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-Agentic%20Workflows-1C3C3C)](https://www.langchain.com/)
[![Ruff](https://img.shields.io/badge/Ruff-Code%20Quality-D7FF64)](https://docs.astral.sh/ruff/)
[![Docs](https://img.shields.io/badge/Docs-Docusaurus-2E8555?logo=docusaurus&logoColor=white)](https://docusaurus.io/)

Autonomous web crawling and Java Playwright Page Object Model generation for scalable UI test automation.

</div>

## Overview

AUTOPOM crawls web applications, extracts interactive UI structure, verifies selector reliability, and generates standardized Java Playwright page objects alongside machine-readable page models.

The project is designed for teams that need predictable POM generation, repeatable crawl workflows, and operational guardrails for enterprise-scale automation pipelines.

## Main Features

- Autonomous crawl orchestration with depth, page, and domain controls.
- Interactive element extraction and semantic page modeling.
- Selector verification and fallback-based self-healing.
- Java Playwright page object generation from structured models.
- Structured persistence (`JSON`, Java classes, crawl summary reports).
- CI-ready quality gates with Ruff formatting and lint checks.

## Core Capabilities

### Intelligent Crawl Orchestration

- Maintains a frontier queue and visited signatures to reduce duplicate page modeling.
- Enforces same-origin boundaries and deny-list domain filtering.
- Builds page-level actions from discovered UI semantics (for example, login flows).

### Model-Driven Generation

- Creates normalized `PageModel` JSON files for each discovered route.
- Converts model sections/elements/actions into Java page object classes.
- Generates a reusable base class and route-specific page files.

### Selector Reliability and Healing

- Validates generated selectors against runtime visibility checks.
- Attempts fallback selectors automatically when primary selectors fail.
- Adjusts confidence scores to support downstream quality decisions.

## Architecture at a Glance

1. Start from a base URL and crawl configuration.
2. Observe page state and extract compact interactive DOM context.
3. Build semantic page and action models.
4. Verify and heal selectors.
5. Generate Java POM artifacts.
6. Persist JSON models, Java code, and crawl reports.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Optional dependency groups:

```bash
python -m pip install -e ".[ai,browser,dev]"
```

## Quick Start

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --max-depth 3 \
  --max-pages 20
```

## Configuration

The crawl engine is configured through `CrawlConfig` (`src/autopom/config.py`).

| Parameter | Default | Description |
|---|---|---|
| `base_url` | required | Root URL where crawling starts. |
| `output_dir` | `output` | Output folder for models, Java artifacts, and reports. |
| `max_depth` | `3` | Maximum link traversal depth from the base URL. |
| `max_pages` | `80` | Maximum number of unique page models to generate. |
| `max_actions_per_page` | `12` | Upper bound for inferred page actions. |
| `same_origin_only` | `true` | Restricts crawling to the base origin. |
| `denied_domains` | predefined list | Excludes social/external domains from traversal. |
| `preferred_testid_attrs` | test-id attributes | Prioritized attributes for robust selectors. |
| `auth_user_env` | `AUTOPOM_USERNAME` | Environment variable name for username. |
| `auth_pass_env` | `AUTOPOM_PASSWORD` | Environment variable name for password. |

## Output Structure

After a run, outputs are created under the selected output directory:

- `models_json/` - JSON page models and metadata per discovered page.
- `java/` - Generated Java Playwright page objects and base page class.
- `reports/crawl_summary.md` - Crawl quality and coverage summary.

## Enterprise Use Cases

### E-commerce Web Applications

- Generate model/code coverage for catalog, product, cart, checkout, and login routes.
- Increase reuse of high-value flows such as add-to-cart and checkout actions.
- Enforce selector quality gates on revenue-critical journeys.

### Internal Portals and Admin Systems

- Discover authenticated role-based workflows with controlled crawl boundaries.
- Capture forms, filters, and tabular interaction patterns consistently.
- Compare generated models between releases to identify UI drift quickly.

## Documentation

- `docs/docs/architecture/overview.md` - platform architecture and flow.
- `docs/docs/guides/agentic-loop.md` - autonomous crawl loop behavior.
- `docs/docs/guides/java-generation.md` - Java POM generation details.
- `docs/docs/guides/self-healing.md` - selector verification and healing.
- `docs/docs/getting-started/quickstart.md` - documentation quickstart.

## Quality and CI

- `ruff check src tests` for linting.
- `ruff format --check src tests` for formatting compliance.
- `python -m unittest discover -s tests -p "test_*_unittest.py" -v` for tests.
- GitHub Actions pipeline validates build, quality, and docs deployment.
