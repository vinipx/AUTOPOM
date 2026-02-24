# Tutorial: First Crawl

## Goal

Run AutoPOM-Agent on a public site and inspect generated outputs.

## Steps

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --pom-language "javascript" \
  --max-depth 2 \
  --max-pages 20
```

## Validate outputs

- Open `output/models_json` for extracted page models.
- Open `output/javascript/pages` for generated classes.
- Open `output/reports/crawl_summary.md` for confidence metrics.

## Try Interactive Mode

For more control over what is captured:

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --interactive \
  --pom-language "typescript"
```

This allows you to verify the page state exactly as the agent sees it before it begins mapping.

## Repeat with TypeScript

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --pom-language "typescript" \
  --max-depth 2 \
  --max-pages 20
```
