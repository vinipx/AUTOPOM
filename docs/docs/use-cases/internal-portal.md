# Use Case: Internal Portal

## Objective

Automate discovery of admin workflows behind role-based authentication.

## Crawl scope

- Start at portal login.
- Traverse navigation modules up to depth 3.
- Capture forms, filters, and table actions.
- Exclude SSO and external BI links.

## Recommendations

- Use role-scoped credential sets.
- Run separate crawls per role for better coverage.
- Compare page models between releases to detect UI drift.
