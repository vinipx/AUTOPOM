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

## Runtime visibility

When running, you will see logs such as:

- `[CRAWL] Visiting ...`
- `[MAP] <PageName> | elements=... | actions=...`
- `[SKIP] ... | reason=...`
