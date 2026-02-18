# Tutorial: Authenticated Crawl

## Goal

Crawl protected routes after login to generate deeper POM coverage.

## Setup credentials

```bash
export AUTOPOM_USERNAME="your-user"
export AUTOPOM_PASSWORD="your-password"
```

## Run crawl

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --base-url "https://app.example.com/login" \
  --output-dir "output" \
  --max-depth 3
```

## Tips

- Use non-production credentials.
- Keep `same_origin_only=true`.
- Restrict depth for faster iterations during tuning.
