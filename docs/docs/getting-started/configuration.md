# Configuration

AutoPOM-Agent behavior is controlled by `CrawlConfig`.

## Core options

| Setting | Purpose | Default |
| --- | --- | --- |
| `base_url` | Entry URL for crawl | required |
| `max_depth` | Maximum recursive depth | `3` |
| `max_pages` | Maximum modeled pages | `80` |
| `max_actions_per_page` | Action budget per page | `12` |
| `same_origin_only` | Restrict to same domain | `true` |
| `denied_domains` | External domains denylist | social domains |
| `output_dir` | Output root for artifacts | `output` |
| `pom_language` | Generated POM language (`java`, `javascript`, `typescript`) | `java` |
| `browser_adapter` | Browser backend (`mock`, `playwright`) | `mock` |
| `playwright_headless` | Run Playwright headless (`true`) or headed (`false`) | `true` |

## Credentials

Use `.env` variables for gated flows:

```bash
AUTOPOM_USERNAME=...
AUTOPOM_PASSWORD=...
```

## CLI equivalent

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://example.com" \
  --output-dir "output" \
  --max-depth 3 \
  --max-pages 20 \
  --pom-language "javascript" \
  --browser-adapter "mock"
```

## Guided execution

Use `bash run.sh` for an interactive flow with enterprise-style prompts:

- URL, language, adapter, depth/pages
- transparent package/browser setup
- final execution preview before run

## Language aliases

- `js` normalizes to `javascript`.
- `ts` normalizes to `typescript`.
- Unsupported values raise a validation error before crawl execution.

## Browser adapter options

- `mock`: deterministic adapter for local testing and CI-safe runs.
- `playwright`: real browser crawl against live web applications.
- CLI shortcut: `--headed` turns off headless mode for Playwright runs.

## Reporting outputs

Every run writes:

- `reports/crawl_summary.md` for crawl quality and selector confidence.
- `reports/execution_summary.md` for stakeholder-friendly run summary.
- `reports/execution_summary.json` for downstream analytics/dashboards.

## Recommended policy baseline

- Keep `max_depth` between `2` and `4`.
- Keep `same_origin_only` enabled.
- Add explicit denylist for external auth/marketing domains.
- Enforce crawl timeout budget in CI runners.
