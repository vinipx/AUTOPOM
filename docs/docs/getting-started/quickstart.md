# Quickstart

## Prerequisites

- Node.js `>=20` for documentation site.
- Python `>=3.11` for AutoPOM-Agent runtime.

## Start docs locally

```bash
cd docs
npm install
npm start
```

## Run AutoPOM-Agent (mock adapter)

```bash
cd ..
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --pom-language "java" \
  --browser-adapter "mock"
```

## Run with guided wizard (recommended)

```bash
bash run.sh
```

The wizard prompts for URL/language/adapter/crawl limits, handles dependency setup transparently, and prints live crawl progress.

## Generated artifacts

- `output/models_json` page models
- `output/<language>` generated Playwright POM classes (`java`, `javascript`, `typescript`)
- `output/reports/crawl_summary.md` run summary
- `output/reports/execution_summary.md` managerial summary (config + metrics + duration)
- `output/reports/execution_summary.json` machine-readable summary payload

## Try another POM language

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --pom-language "typescript"
```

## Real browser crawl (Playwright)

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

## Interactive Capture Mode

Use this mode if you need to log in manually or navigate to a specific page before starting the mapping process:

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --interactive \
  --pom-language "typescript"
```

1. A browser will open.
2. Perform any manual steps (Login, Navigation).
3. Return to the terminal and press **ENTER**.
4. AutoPOM will capture the current page and generate the POM.

## Capture from Existing Browser

If you already have a browser open with remote debugging enabled:

```bash
# Launch Chrome first:
# google-chrome --remote-debugging-port=9222

PYTHONPATH=src python3 -m autopom.cli.main \
  --capture http://localhost:9222 \
  --pom-language "java"
```

## Runtime visibility

When running, you will see logs such as:

- `[CRAWL] Visiting ...`
- `[MAP] <PageName> | elements=... | actions=...`
- `[SKIP] ... | reason=...`
