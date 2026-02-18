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


class JavaGenerator:
    def __init__(
        self, output_dir: Path, template_dir: Path, config: JavaGeneratorConfig
    ) -> None:
        self.output_dir = output_dir
        self.template_dir = template_dir
        self.config = config
        (self.output_dir / "java" / "pages").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "java" / "base").mkdir(parents=True, exist_ok=True)

    def generate_base_page(self) -> Path:
        target = self.output_dir / "java" / "base" / "BasePage.java"
        target.write_text(self._render_base_page(), encoding="utf-8")
        return target

    def generate_page(self, page: PageModel) -> Path:
        flattened = [e for section in page.sections for e in section.elements]
        elements = [
            {"field_name": _to_field_name(e.element_id), "selector": e.selector}
            for e in flattened
        ]
        methods = self._build_methods(page)
        target = self.output_dir / "java" / "pages" / f"{page.page_name}.java"
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
            body.append("return this;")
            method = {
                "return_type": page.page_name,
                "name": action.name,
                "params": ", ".join(f"String {p}" for p in action.params),
                "body": body,
            }
            methods.append(method)
        return methods

    @staticmethod
    def _translate_step(step: str) -> str | None:
        if step.startswith("fill("):
            inside = step[len("fill(") : -1]
            target, arg = [part.strip() for part in inside.split(",", 1)]
            return f"{_to_field_name(target)}.fill({arg});"
        if step.startswith("click("):
            inside = step[len("click(") : -1].strip()
            return f"{_to_field_name(inside)}.click();"
        return f"// TODO: translate step: {step}"

    def _render_base_page(self) -> str:
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
