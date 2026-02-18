# Tutorial: First Crawl

## Goal

Run AutoPOM-Agent on a public site and inspect generated outputs.

## Steps

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --max-depth 2 \
  --max-pages 20
```

## Validate outputs

- Open `output/models_json` for extracted page models.
- Open `output/java/pages` for generated classes.
- Open `output/reports/crawl_summary.md` for confidence metrics.
