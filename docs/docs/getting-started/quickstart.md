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
  --pom-language "java"
```

## Generated artifacts

- `output/models_json` page models
- `output/<language>` generated Playwright POM classes (`java`, `javascript`, `typescript`)
- `output/reports/crawl_summary.md` run summary

## Try another POM language

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --pom-language "typescript"
```
