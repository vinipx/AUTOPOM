<div align="center">

# AUTOPOM

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-Agentic%20Workflows-1C3C3C)](https://www.langchain.com/)
[![Ruff](https://img.shields.io/badge/Ruff-Code%20Quality-D7FF64)](https://docs.astral.sh/ruff/)
[![Docs](https://img.shields.io/badge/Docs-Docusaurus-2E8555?logo=docusaurus&logoColor=white)](https://docusaurus.io/)

Autonomous web crawling and Playwright Page Object Model generation in Java, JavaScript, and TypeScript.

</div>

## Overview

AUTOPOM crawls web applications, extracts interactive UI structure, verifies selector reliability, and generates standardized Playwright page objects (Java, JavaScript, or TypeScript) alongside machine-readable page models.

The project is designed for teams that need predictable POM generation, repeatable crawl workflows, and operational guardrails for enterprise-scale automation pipelines.

## Main Features

- **Interactive Run Wizard**: Guided prompt flow for easy configuration and setup.
- **Interactive Capture Mode**: Manually navigate or authenticate in a live browser before mapping.
- **Existing Browser Capture**: Attach to an already running browser instance via CDP.
- **Chrome Profile Support**: Use your existing browser sessions, cookies, and saved passwords.
- **Autonomous Crawl Orchestration**: Controlled depth, page limits, and domain boundaries.
- **Semantic Page Modeling**: Extract interactive UI structure and infer meaningful element names.
- **Multi-language POM Generation**: Standardized Playwright page objects in `java`, `javascript`, and `typescript`.
- **Selector Self-healing**: Automatic verification and fallback promotion for resilient locators.
- **Operational Visibility**: Live crawl logs and comprehensive managerial/technical reports.

## Core Capabilities

### Interactive & Hybrid Workflows

- **Headed Interaction**: Launch a visible browser, perform manual steps (like MFA or complex navigation), and capture when ready.
- **Session Reuse**: Leverage existing Chrome profiles to skip authentication steps and crawl protected areas of your application.
- **Targeted Mapping**: Attach to any open tab on a local or remote browser instance for surgical POM generation.

### Intelligent Crawl Orchestration

- Maintains a frontier queue and visited signatures to reduce duplicate page modeling.
- Enforces same-origin boundaries and deny-list domain filtering.
- Builds page-level actions from discovered UI semantics (for example, login flows).

### Model-Driven Generation

- Creates normalized `PageModel` JSON files for each discovered route.
- Converts model sections/elements/actions into language-specific page object classes.
- Generates a reusable base class and route-specific page files for the selected target language.

### Selector Reliability and Healing

- Validates generated selectors against runtime visibility checks.
- Attempts fallback selectors automatically when primary selectors fail.
- Adjusts confidence scores to support downstream quality decisions.

### Operational Visibility and Reporting

- Shows live crawl progress with page/depth/queue visibility while running.
- Produces both technical and managerial reports at run completion.
- Captures effective configuration, performance timing, and output metrics for traceability.

## Architecture at a Glance

1. Start from a base URL and crawl configuration.
2. Observe page state and extract compact interactive DOM context.
3. Build semantic page and action models.
4. Verify and heal selectors.
5. Generate POM artifacts for the configured language.
6. Persist JSON models, generated code, and crawl reports.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[ai,browser,dev]"
```

### Setup Pre-commit Hooks (Recommended)

To guarantee code quality and formatting before every commit/push:

```bash
pre-commit install
```

This will automatically run `ruff` and syntax checks on your changed files.

## Quick Start

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --pom-language "typescript" \
  --browser-adapter "mock" \
  --max-depth 3 \
  --max-pages 20
```

Supported values for `--pom-language`: `java`, `javascript`, `typescript`.
Supported values for `--browser-adapter`: `mock`, `playwright`.

## Interactive Run Wizard

Use the guided runner for a user-friendly prompt flow:

```bash
bash run.sh
```

It asks for base URL, output folder, language, browser adapter (`mock` or `playwright`), and crawl limits, then automatically installs required Python packages and Playwright browser runtime when needed.

Dependency setup is optimized: if packages and browser runtime are already up to date, the script skips reinstallation automatically.

During execution, users get live logs for crawl and mapping activity, plus a final execution summary report.

## Configuration

The crawl engine is configured through `CrawlConfig` (`src/autopom/config.py`).

| Parameter | Default | Description |
|---|---|---|
| `base_url` | required | Root URL where crawling starts. |
| `output_dir` | `output` | Output folder for models, code artifacts, and reports. |
| `max_depth` | `3` | Maximum link traversal depth from the base URL. |
| `max_pages` | `80` | Maximum number of unique page models to generate. |
| `max_actions_per_page` | `12` | Upper bound for inferred page actions. |
| `same_origin_only` | `true` | Restricts crawling to the base origin. |
| `denied_domains` | predefined list | Excludes social/external domains from traversal. |
| `preferred_testid_attrs` | test-id attributes | Prioritized attributes for robust selectors. |
| `auth_user_env` | `AUTOPOM_USERNAME` | Environment variable name for username. |
| `auth_pass_env` | `AUTOPOM_PASSWORD` | Environment variable name for password. |
| `pom_language` | `java` | POM output language (`java`, `javascript`, `typescript`). |
| `locator_storage` | `inline` | Selector storage strategy (`inline`, `external`). |
| `browser_adapter` | `mock` | Browser runtime (`mock`, `playwright`). |
| `playwright_headless` | `true` | Use headless browser for Playwright. |
| `cdp_url` | `None` | Connect to an existing browser via CDP URL. |
| `chrome_profile` | `false` | Use the default local Chrome profile. |

## Output Structure

After a run, outputs are created under the selected output directory:

- `models_json/` - JSON page models and metadata per discovered page.
- `<language>/` - Generated Playwright page objects and base page class.
- `reports/crawl_summary.md` - Crawl quality and selector confidence summary.
- `reports/execution_summary.md` - Human-readable managerial summary.
- `reports/execution_summary.json` - Structured summary payload for automation.

## Usage Examples

### Interactive Capture (Headed)

Launch a browser, log in manually, and capture the page:

```bash
PYTHONPATH=src python3 -m autopom.cli.main --interactive --pom-language typescript
```

### Existing Browser (CDP)

Capture from a browser already running with remote debugging enabled:

```bash
# First, launch Chrome with remote debugging
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Then run AutoPOM
PYTHONPATH=src python3 -m autopom.cli.main --capture http://localhost:9222
```

### Multi-language Generation

```bash
# Java (default)
PYTHONPATH=src python3 -m autopom.cli.main --base-url "https://example.com" --pom-language java

# JavaScript
PYTHONPATH=src python3 -m autopom.cli.main --base-url "https://example.com" --pom-language javascript

# TypeScript
PYTHONPATH=src python3 -m autopom.cli.main --base-url "https://example.com" --pom-language typescript
```

### Live crawl with Playwright

```bash
python -m pip install -e ".[browser]"
python -m playwright install chromium

PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://vinipx.github.io/AUTOPOM/" \
  --output-dir "output-live" \
  --pom-language "typescript" \
  --browser-adapter "playwright" \
  --max-depth 2 \
  --max-pages 20
```

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
- `docs/docs/guides/java-generation.md` - multi-language POM generation details.
- `docs/docs/guides/self-healing.md` - selector verification and healing.
- `docs/docs/getting-started/quickstart.md` - documentation quickstart.

## Quality and CI

- `ruff check src tests` for linting.
- `ruff format --check src tests` for formatting compliance.
- `python -m unittest discover -s tests -p "test_*_unittest.py" -v` for tests.
- GitHub Actions pipeline validates build, quality, and docs deployment.
