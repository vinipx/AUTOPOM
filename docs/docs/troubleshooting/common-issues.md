# Troubleshooting

## Crawl appears stuck

- Lower `max_depth` and `max_pages`.
- Verify cycle detection signatures are changing.
- Confirm external domains are denied.

## Too many duplicate pages

- Improve URL normalization rules.
- Include route-relevant query params only.
- Add stronger landmark/DOM fingerprinting.

## Unstable selectors in output

- Prioritize `data-testid` attributes in app code.
- Increase fallback selector depth.
- Enable additional post-generation validation passes.

## Missing protected routes

- Provide valid credentials through environment variables.
- Ensure login flow is reachable and not blocked by CAPTCHAs.
