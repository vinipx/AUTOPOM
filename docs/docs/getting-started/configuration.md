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

## Credentials

Use `.env` variables for gated flows:

```bash
AUTOPOM_USERNAME=...
AUTOPOM_PASSWORD=...
```

## Recommended policy baseline

- Keep `max_depth` between `2` and `4`.
- Keep `same_origin_only` enabled.
- Add explicit denylist for external auth/marketing domains.
- Enforce crawl timeout budget in CI runners.
