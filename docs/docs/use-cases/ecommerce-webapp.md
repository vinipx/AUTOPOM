# Use Case: E-commerce Web App

## Objective

Generate POM coverage for catalog, product detail, cart, and checkout across multiple automation language stacks.

## Crawl scope

- Start from storefront home route.
- Include product listing and detail pages.
- Enable authenticated checkout flows.
- Exclude payment provider external pages.

## Key generated pages

- `HomePage`
- `ProductPage`
- `CartPage`
- `CheckoutPage`
- `LoginPage`

## Success criteria

- At least 90% selector verification pass rate in checkout-critical pages.
- Reusable action methods for add-to-cart and checkout steps.
- Language-targeted output for team stack:
  - `output/java` for Java-based QA platforms.
  - `output/javascript` or `output/typescript` for JS/TS-native frameworks.
