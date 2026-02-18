# Element Mapping

Element mapping combines **DOM context** and **visual reasoning**.

## Mapping order

1. Stable DOM attributes (`data-testid`, `data-qa`)
2. Accessibility semantics (role + accessible name)
3. Label/input relationships
4. Scoped text selectors
5. Visual fallback for icon-only controls

## Naming standards

- Use camelCase action-oriented names:
  - `signInButton`
  - `usernameInput`
  - `closeModalButton`
- Avoid visual-only names (`blueButton`, `icon3`)

## Dynamic IDs/classes

Avoid brittle selectors like runtime-generated IDs and hashed classes.
Always store ranked fallback selectors for resilience.
