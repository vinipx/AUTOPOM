from __future__ import annotations

from dataclasses import dataclass
import json
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
SUPPORTED_LOCATOR_STORAGE = ("inline", "external")


def normalize_pom_language(language: str) -> str:
    normalized = language.strip().lower()
    aliases = {"js": "javascript", "ts": "typescript"}
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_POM_LANGUAGES:
        allowed = ", ".join(SUPPORTED_POM_LANGUAGES)
        raise ValueError(f"Unsupported pom language '{language}'. Allowed: {allowed}.")
    return normalized


def normalize_locator_storage(locator_storage: str) -> str:
    normalized = locator_storage.strip().lower()
    aliases = {"ext": "external"}
    normalized = aliases.get(normalized, normalized)
    if normalized not in SUPPORTED_LOCATOR_STORAGE:
        allowed = ", ".join(SUPPORTED_LOCATOR_STORAGE)
        raise ValueError(
            f"Unsupported locator storage '{locator_storage}'. Allowed: {allowed}."
        )
    return normalized


class PlaywrightPomGenerator:
    def __init__(
        self,
        output_dir: Path,
        language: str,
        locator_storage: str = "inline",
        template_dir: Path | None = None,
        java_config: JavaGeneratorConfig | None = None,
    ) -> None:
        self.output_dir = output_dir
        self.language = normalize_pom_language(language)
        self.locator_storage = normalize_locator_storage(locator_storage)
        self.template_dir = template_dir
        self.config = java_config or JavaGeneratorConfig()

        language_dir = self.output_dir / self.language
        (language_dir / "pages").mkdir(parents=True, exist_ok=True)
        (language_dir / "base").mkdir(parents=True, exist_ok=True)
        (language_dir / "locators").mkdir(parents=True, exist_ok=True)

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
        if self.locator_storage == "external":
            self._generate_locator_finder()
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
        if self.locator_storage == "external":
            self._write_external_locators(page.page_name, elements)
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
        if self.locator_storage == "external":
            lines.insert(3, f"import {p}.base.LocatorFinder;")
        for element in elements:
            lines.append(f"    private final Locator {element['field_name']};")
        lines.extend(
            [
                "",
                (
                    f"    public {page_name}(Page page, LocatorFinder locatorFinder) "
                    + "{"
                    if self.locator_storage == "external"
                    else f"    public {page_name}(Page page) " + "{"
                ),
                "        super(page);",
            ]
        )
        for element in elements:
            if self.locator_storage == "external":
                lines.append(
                    f'        this.{element["field_name"]} = locator(locatorFinder.get("{element["field_name"]}"));'
                )
            else:
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
        lines: list[str] = ['const { BasePage } = require("../base/BasePage");']
        if self.locator_storage == "external":
            lines.append('const { LocatorFinder } = require("../base/locatorFinder");')
        lines.extend(["", f"class {page_name} extends BasePage " + "{"])
        if self.locator_storage == "external":
            lines.extend(
                [
                    "  constructor(page, locatorFinder) {",
                    "    super(page);",
                    f'    const finder = locatorFinder || new LocatorFinder(process.cwd() + "/{self.language}/locators", "{page_name}");',
                ]
            )
        else:
            lines.extend(["  constructor(page) {", "    super(page);"])
        for element in elements:
            if self.locator_storage == "external":
                lines.append(
                    f'    this.{element["field_name"]} = this.locator(finder.get("{element["field_name"]}"));'
                )
            else:
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
        lines: list[str] = ['import { Locator, Page } from "@playwright/test";']
        lines.append('import { BasePage } from "../base/BasePage";')
        if self.locator_storage == "external":
            lines.append('import { LocatorFinder } from "../base/LocatorFinder";')
        lines.extend(["", f"export class {page_name} extends BasePage " + "{"])
        for element in elements:
            lines.append(f"  private readonly {element['field_name']}: Locator;")
        if self.locator_storage == "external":
            lines.extend(
                [
                    "",
                    "  constructor(page: Page, locatorFinder?: LocatorFinder) {",
                    "    super(page);",
                    f'    const finder = locatorFinder ?? new LocatorFinder(`${{process.cwd()}}/{self.language}/locators`, "{page_name}");',
                ]
            )
        else:
            lines.extend(["", "  constructor(page: Page) {", "    super(page);"])

        for element in elements:
            if self.locator_storage == "external":
                lines.append(
                    f'    this.{element["field_name"]} = this.locator(finder.get("{element["field_name"]}"));'
                )
            else:
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

    def _write_external_locators(self, page_name: str, elements: list[dict]) -> Path:
        locators_dir = self.output_dir / self.language / "locators"
        if self.language == "java":
            target = locators_dir / f"{page_name}.properties"
            lines = []
            for element in elements:
                selector = (
                    element["selector"]
                    .replace("\\", "\\\\")
                    .replace("\n", "\\n")
                    .replace("=", "\\=")
                    .replace(":", "\\:")
                )
                lines.append(f"{element['field_name']}={selector}")
            target.write_text(
                "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8"
            )
            return target

        target = locators_dir / f"{page_name}.json"
        payload = {element["field_name"]: element["selector"] for element in elements}
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return target

    def _generate_locator_finder(self) -> Path:
        base_dir = self.output_dir / self.language / "base"
        if self.language == "java":
            target = base_dir / "LocatorFinder.java"
            p = self.config.base_package
            target.write_text(
                (
                    f"package {p}.base;\n\n"
                    "import java.io.IOException;\n"
                    "import java.io.InputStream;\n"
                    "import java.nio.file.Files;\n"
                    "import java.nio.file.Path;\n"
                    "import java.util.Properties;\n\n"
                    "public final class LocatorFinder {\n"
                    "    private final Properties props;\n\n"
                    "    private LocatorFinder(Properties props) {\n"
                    "        this.props = props;\n"
                    "    }\n\n"
                    "    public static LocatorFinder forPage(Path locatorRoot, String pageName) {\n"
                    "        Properties props = new Properties();\n"
                    '        Path source = locatorRoot.resolve(pageName + ".properties");\n'
                    "        try (InputStream in = Files.newInputStream(source)) {\n"
                    "            props.load(in);\n"
                    "        } catch (IOException ex) {\n"
                    '            throw new IllegalStateException("Unable to load locator file: " + source, ex);\n'
                    "        }\n"
                    "        return new LocatorFinder(props);\n"
                    "    }\n\n"
                    "    public String get(String key) {\n"
                    "        String value = props.getProperty(key);\n"
                    "        if (value == null || value.isBlank()) {\n"
                    '            throw new IllegalArgumentException("Missing locator key: " + key);\n'
                    "        }\n"
                    "        return value;\n"
                    "    }\n"
                    "}\n"
                ),
                encoding="utf-8",
            )
            return target

        if self.language == "javascript":
            target = base_dir / "locatorFinder.js"
            target.write_text(
                (
                    "const fs = require('fs');\n"
                    "const path = require('path');\n\n"
                    "class LocatorFinder {\n"
                    "  constructor(locatorRoot, pageName) {\n"
                    "    const source = path.join(locatorRoot, `${pageName}.json`);\n"
                    "    this.locators = JSON.parse(fs.readFileSync(source, 'utf-8'));\n"
                    "  }\n\n"
                    "  get(key) {\n"
                    "    const value = this.locators[key];\n"
                    "    if (!value) {\n"
                    "      throw new Error(`Missing locator key: ${key}`);\n"
                    "    }\n"
                    "    return value;\n"
                    "  }\n"
                    "}\n\n"
                    "module.exports = { LocatorFinder };\n"
                ),
                encoding="utf-8",
            )
            return target

        target = base_dir / "LocatorFinder.ts"
        target.write_text(
            (
                'import fs from "fs";\n'
                'import path from "path";\n\n'
                "export class LocatorFinder {\n"
                "  private readonly locators: Record<string, string>;\n\n"
                "  constructor(locatorRoot: string, pageName: string) {\n"
                "    const source = path.join(locatorRoot, `${pageName}.json`);\n"
                "    this.locators = JSON.parse(fs.readFileSync(source, 'utf-8')) as Record<string, string>;\n"
                "  }\n\n"
                "  get(key: string): string {\n"
                "    const value = this.locators[key];\n"
                "    if (!value) {\n"
                "      throw new Error(`Missing locator key: ${key}`);\n"
                "    }\n"
                "    return value;\n"
                "  }\n"
                "}\n"
            ),
            encoding="utf-8",
        )
        return target


class JavaGenerator(PlaywrightPomGenerator):
    def __init__(
        self, output_dir: Path, template_dir: Path, config: JavaGeneratorConfig
    ) -> None:
        super().__init__(
            output_dir=output_dir,
            language="java",
            locator_storage="inline",
            template_dir=template_dir,
            java_config=config,
        )
