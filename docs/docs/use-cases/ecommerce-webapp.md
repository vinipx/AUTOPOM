# Use Case: E-commerce Web App

## Objective

Generate POM coverage for catalog, product detail, cart, and checkout.

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
