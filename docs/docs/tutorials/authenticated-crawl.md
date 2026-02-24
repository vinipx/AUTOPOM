# Tutorial: Authenticated Crawl

## Goal

Crawl protected routes after login to generate deeper POM coverage. AutoPOM provides three main ways to handle authenticated applications.

## 1. Interactive Mode (Recommended for MFA)

If your application requires Multi-Factor Authentication (MFA) or complex manual steps:

```bash
PYTHONPATH=src python3 -m autopom.cli.main \
  --interactive \
  --pom-language "typescript"
```

- AutoPOM will launch a visible browser and pause.
- You perform the login and MFA manually.
- Press **ENTER** in the terminal when ready.
- AutoPOM captures the current state and continues the crawl from there.

## 2. Chrome Profile Mode

If you are already logged in to your application in your regular Google Chrome browser:

```bash
# Ensure all Chrome instances are closed first
PYTHONPATH=src python3 -m autopom.cli.main \
  --chrome-profile \
  --base-url "https://app.example.com/dashboard"
```

AutoPOM will inherit your existing cookies and sessions, often bypassing the login screen entirely.

## 3. Environment Variables (Headless/CI)

For automated pipelines or simple login forms:

## Tips

- Use non-production credentials.
- Keep `same_origin_only=true`.
- Restrict depth for faster iterations during tuning.
