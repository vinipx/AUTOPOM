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
PYTHONPATH=src python3 -m autopom.cli.main --base-url "https://example.com" --output-dir "output"
```

## Generated artifacts

- `output/models_json` page models
- `output/java` generated Java classes
- `output/reports/crawl_summary.md` run summary
