# POM Generation Pipeline (Java, JavaScript, TypeScript)

Code generation is model-driven and language-configurable. AUTOPOM generates output from `PageModel` artifacts, not directly from crawl events.

## Pipeline

1. Build `PageModel` JSON from extraction stage.
2. Verify/heal selectors and update confidence.
3. Resolve target language via `pom_language`.
4. Render language-specific classes:
   - `BasePage.<ext>`
   - `<PageName>.<ext>`
5. Persist to `output/<language>`.

## Supported output languages

| Language | CLI value | Extension | Output folder |
| --- | --- | --- | --- |
| Java | `java` | `.java` | `output/java` |
| JavaScript | `javascript` | `.js` | `output/javascript` |
| TypeScript | `typescript` | `.ts` | `output/typescript` |

## Locator Storage Strategy

You can control how selectors are stored in the generated code using the `locator_storage` parameter:

- **`inline`**: Selectors are embedded directly in the class fields or methods. This is standard for most Playwright implementations.
- **`external`**: Selectors are stored in a sidecar metadata file, keeping the Page Object class focused purely on interaction logic.

## Selection strategy

- Set `--pom-language` in CLI or `pom_language` in `CrawlConfig`.
- Keep language-specific style differences inside the generator layer.
- Reuse the same semantic schema and action translation logic for all languages.

## Clean code rules

- Encapsulated locator fields in generated page classes.
- Public intent-level methods (`login`, `searchProduct`, `submitOrder`).
- Descriptive naming and minimal UI implementation leakage.
- Base page abstraction shared by all generated page classes.

## Example generated actions

```java
public LoginPage login(String username, String password) {
    usernameInput.fill(username);
    passwordInput.fill(password);
    signInButton.click();
    return this;
}
```

```typescript
async login(username: string, password: string): Promise<LoginPage> {
  await this.usernameInput.fill(username)
  await this.passwordInput.fill(password)
  await this.signInButton.click()
  return this
}
```
