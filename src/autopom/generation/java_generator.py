from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from autopom.extraction.schema import PageModel


def _to_field_name(element_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", element_id)
    return cleaned[:1].lower() + cleaned[1:] if cleaned else "element"


@dataclass(slots=True)
class JavaGeneratorConfig:
    base_package: str = "com.autopom"


SUPPORTED_POM_LANGUAGES = ("java", "javascript", "typescript")


def normalize_pom_language(language: str) -> str:
    normalized = language.strip().lower()
    aliases = {"js": "javascript", "ts": "typescript"}
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_POM_LANGUAGES:
        allowed = ", ".join(SUPPORTED_POM_LANGUAGES)
        raise ValueError(f"Unsupported pom language '{language}'. Allowed: {allowed}.")
    return normalized


class PlaywrightPomGenerator:
    def __init__(
        self,
        output_dir: Path,
        language: str,
        template_dir: Path | None,
        java_config: JavaGeneratorConfig | None = None,
    ) -> None:
        self.output_dir = output_dir
        self.language = normalize_pom_language(language)
        self.template_dir = template_dir
        self.config = java_config or JavaGeneratorConfig()

        language_dir = self.output_dir / self.language
        (language_dir / "pages").mkdir(parents=True, exist_ok=True)
        (language_dir / "base").mkdir(parents=True, exist_ok=True)

    @property
    def file_extension(self) -> str:
        if self.language == "java":
            return ".java"
        if self.language == "javascript":
            return ".js"
        return ".ts"

    def generate_base_page(self) -> Path:
        target = (
            self.output_dir / self.language / "base" / f"BasePage{self.file_extension}"
        )
        target.write_text(self._render_base_page(), encoding="utf-8")
        return target

    def generate_page(self, page: PageModel) -> Path:
        flattened = [e for section in page.sections for e in section.elements]
        elements = [
            {"field_name": _to_field_name(e.element_id), "selector": e.selector}
            for e in flattened
        ]
        methods = self._build_methods(page)
        target = (
            self.output_dir
            / self.language
            / "pages"
            / f"{page.page_name}{self.file_extension}"
        )
        target.write_text(
            self._render_page(page.page_name, elements, methods), encoding="utf-8"
        )
        return target

    def _build_methods(self, page: PageModel) -> list[dict]:
        methods: list[dict] = []
        for action in page.actions:
            body: list[str] = []
            for step in action.steps:
                rendered = self._translate_step(step)
                if rendered:
                    body.append(rendered)
            if action.post_condition:
                body.append(
                    f"// TODO: validate post-condition: {action.post_condition}"
                )
            body.append("return this;" if self.language == "java" else "return this")
            params = self._render_params(action.params)
            method = {
                "return_type": self._render_return_type(page.page_name),
                "name": action.name,
                "params": params,
                "body": body,
            }
            methods.append(method)
        return methods

    def _render_params(self, params: list[str]) -> str:
        if self.language == "java":
            return ", ".join(f"String {p}" for p in params)
        if self.language == "typescript":
            return ", ".join(f"{p}: string" for p in params)
        return ", ".join(params)

    def _render_return_type(self, page_name: str) -> str:
        if self.language == "java":
            return page_name
        if self.language == "typescript":
            return f"Promise<{page_name}>"
        return ""

    def _translate_step(self, step: str) -> str | None:
        await_prefix = "" if self.language == "java" else "await this."
        if step.startswith("fill("):
            inside = step[len("fill(") : -1]
            target, arg = [part.strip() for part in inside.split(",", 1)]
            if self.language == "java":
                return f"{_to_field_name(target)}.fill({arg});"
            return f"{await_prefix}{_to_field_name(target)}.fill({arg})"
        if step.startswith("click("):
            inside = step[len("click(") : -1].strip()
            if self.language == "java":
                return f"{_to_field_name(inside)}.click();"
            return f"{await_prefix}{_to_field_name(inside)}.click()"
        return f"// TODO: translate step: {step}"

    def _render_base_page(self) -> str:
        if self.language == "javascript":
            return (
                "class BasePage {\n"
                "  constructor(page) {\n"
                "    this.page = page;\n"
                "  }\n\n"
                "  locator(selector) {\n"
                "    return this.page.locator(selector);\n"
                "  }\n"
                "}\n\n"
                "module.exports = { BasePage };\n"
            )
        if self.language == "typescript":
            return (
                'import { Locator, Page } from "@playwright/test";\n\n'
                "export abstract class BasePage {\n"
                "  protected readonly page: Page;\n\n"
                "  protected constructor(page: Page) {\n"
                "    this.page = page;\n"
                "  }\n\n"
                "  protected locator(selector: string): Locator {\n"
                "    return this.page.locator(selector);\n"
                "  }\n"
                "}\n"
            )

        p = self.config.base_package
        return (
            f"package {p}.base;\n\n"
            "import com.microsoft.playwright.Locator;\n"
            "import com.microsoft.playwright.Page;\n\n"
            "public abstract class BasePage {\n"
            "    protected final Page page;\n\n"
            "    protected BasePage(Page page) {\n"
            "        this.page = page;\n"
            "    }\n\n"
            "    protected Locator locator(String selector) {\n"
            "        return page.locator(selector);\n"
            "    }\n"
            "}\n"
        )

    def _render_page(
        self, page_name: str, elements: list[dict], methods: list[dict]
    ) -> str:
        if self.language == "javascript":
            return self._render_javascript_page(page_name, elements, methods)
        if self.language == "typescript":
            return self._render_typescript_page(page_name, elements, methods)

        p = self.config.base_package
        lines: list[str] = [
            f"package {p}.pages;",
            "",
            f"import {p}.base.BasePage;",
            "import com.microsoft.playwright.Locator;",
            "import com.microsoft.playwright.Page;",
            "",
            f"public class {page_name} extends BasePage " + "{",
        ]
        for element in elements:
            lines.append(f"    private final Locator {element['field_name']};")
        lines.extend(
            [
                "",
                f"    public {page_name}(Page page) " + "{",
                "        super(page);",
            ]
        )
        for element in elements:
            selector = element["selector"].replace('"', '\\"')
            lines.append(
                f'        this.{element["field_name"]} = locator("{selector}");'
            )
        lines.append("    }")
        lines.append("")

        for method in methods:
            params = method["params"]
            lines.append(
                f"    public {method['return_type']} {method['name']}({params}) " + "{"
            )
            for stmt in method["body"]:
                lines.append(f"        {stmt}")
            lines.append("    }")
            lines.append("")

        lines.append("}")
        return "\n".join(lines)

    @staticmethod
    def _escape_selector(selector: str) -> str:
        return selector.replace("\\", "\\\\").replace('"', '\\"')

    def _render_javascript_page(
        self, page_name: str, elements: list[dict], methods: list[dict]
    ) -> str:
        lines: list[str] = [
            'const { BasePage } = require("../base/BasePage");',
            "",
            f"class {page_name} extends BasePage " + "{",
            "  constructor(page) {",
            "    super(page);",
        ]
        for element in elements:
            selector = self._escape_selector(element["selector"])
            lines.append(
                f'    this.{element["field_name"]} = this.locator("{selector}");'
            )
        lines.extend(["  }", ""])

        for method in methods:
            params = method["params"]
            lines.append(f"  async {method['name']}({params}) " + "{")
            for stmt in method["body"]:
                lines.append(f"    {stmt}")
            lines.append("  }")
            lines.append("")

        lines.extend(["}", "", f"module.exports = {{ {page_name} }};"])
        return "\n".join(lines)

    def _render_typescript_page(
        self, page_name: str, elements: list[dict], methods: list[dict]
    ) -> str:
        lines: list[str] = [
            'import { Locator, Page } from "@playwright/test";',
            'import { BasePage } from "../base/BasePage";',
            "",
            f"export class {page_name} extends BasePage " + "{",
        ]
        for element in elements:
            lines.append(f"  private readonly {element['field_name']}: Locator;")
        lines.extend(["", "  constructor(page: Page) {", "    super(page);"])

        for element in elements:
            selector = self._escape_selector(element["selector"])
            lines.append(
                f'    this.{element["field_name"]} = this.locator("{selector}");'
            )
        lines.extend(["  }", ""])

        for method in methods:
            params = method["params"]
            lines.append(
                f"  async {method['name']}({params}): {method['return_type']} " + "{"
            )
            for stmt in method["body"]:
                lines.append(f"    {stmt}")
            lines.append("  }")
            lines.append("")

        lines.append("}")
        return "\n".join(lines)


class JavaGenerator(PlaywrightPomGenerator):
    def __init__(
        self, output_dir: Path, template_dir: Path, config: JavaGeneratorConfig
    ) -> None:
        super().__init__(
            output_dir=output_dir,
            language="java",
            template_dir=template_dir,
            java_config=config,
        )
