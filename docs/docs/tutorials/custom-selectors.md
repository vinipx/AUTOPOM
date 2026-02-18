# Tutorial: Custom Selector Policies

## Goal

Improve selector reliability for component-heavy frontends.

## Strategy

- Prioritize custom data attributes:
  - `data-testid`
  - `data-qa`
- Add section-scoped fallback policies for duplicated controls.
- Avoid generated IDs and unstable hashed classes.

## Recommended extension points

- Extend fallback ranking rules in extraction/mapping modules.
- Add project-specific naming overrides for known patterns.
- Add post-generation smoke tests against critical pages.
