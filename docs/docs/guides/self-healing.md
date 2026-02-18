# Self-Healing Selectors

Before selectors are persisted, AutoPOM-Agent validates them immediately.

## Verification sequence

1. Check primary selector visibility.
2. If failed, evaluate fallback selectors in rank order.
3. Promote first valid fallback as new primary selector.
4. Re-score selector confidence.
5. Flag unresolved elements for manual review.

## Why it matters

- Prevents propagating broken locators into generated language-specific code.
- Improves first-pass reliability of generated POM classes.
- Reduces test maintenance after UI changes.

## Recommended threshold policy

- `>= 0.90`: safe for direct generation
- `0.70 - 0.89`: generate with warning
- `< 0.70`: require review
