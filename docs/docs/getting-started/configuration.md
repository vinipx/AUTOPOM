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
  --pom-language "javascript"
```

## Language aliases

- `js` normalizes to `javascript`.
- `ts` normalizes to `typescript`.
- Unsupported values raise a validation error before crawl execution.

## Recommended policy baseline

- Keep `max_depth` between `2` and `4`.
- Keep `same_origin_only` enabled.
- Add explicit denylist for external auth/marketing domains.
- Enforce crawl timeout budget in CI runners.
