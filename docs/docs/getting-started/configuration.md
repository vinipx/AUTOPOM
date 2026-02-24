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
| `locator_storage` | Selector storage strategy (`inline`, `external`) | `inline` |
| `browser_adapter` | Browser backend (`mock`, `playwright`) | `mock` |
| `playwright_headless` | Run Playwright headless (`true`) or headed (`false`) | `true` |
| `cdp_url` | Connect to existing browser via CDP URL | `None` |
| `chrome_profile` | Use local Chrome profile for sessions | `false` |
| `interactive_pause` | Wait for user input before capturing | `false` |

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
  --browser-adapter "playwright" \
  --interactive
```

## Advanced Browser Flags

### Interactive Mode (`--interactive`)

Launches a headed browser and pauses execution. This is the recommended way to handle complex authentication (MFA, Captchas) or to navigate to a specific application state before triggering the crawl.

### Existing Browser (`--capture` or `-c`)

Attaches to a browser already running with the `--remote-debugging-port=9222` flag.
- Usage: `--capture http://localhost:9222`
- Default if no URL provided: `http://localhost:9222`

### Chrome Profile (`--chrome-profile`)

Launches a new instance using your default Google Chrome profile. This inherits all your active sessions, cookies, and stored credentials.
**Note:** All existing Chrome windows must be closed before using this flag to avoid profile lock errors.

## Generation Options

### Locator Storage (`--locator-storage`)

- `inline` (default): Locators are defined directly within the Page Object methods or fields.
- `external`: Locators are stored in a separate metadata file (coming soon for all languages), allowing for easier updates without modifying code.

## Language aliases

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
