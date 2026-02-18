# Java Generation Pipeline

Java code is generated from page models, not directly from crawl events.

## Pipeline

1. Build `PageModel` JSON from extraction stage.
2. Verify/heal selectors and update confidence.
3. Render templates for:
   - `BasePage.java`
   - `<PageName>.java`
4. Persist to `output/java`.

## Clean code rules

- Private locator fields.
- Public intent-level methods (`login`, `searchProduct`, `submitOrder`).
- Descriptive naming and minimal UI implementation leakage.

## Example generated action

```java
public LoginPage login(String username, String password) {
    usernameInput.fill(username);
    passwordInput.fill(password);
    signInButton.click();
    return this;
}
```
