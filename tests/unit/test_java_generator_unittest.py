from pathlib import Path
import tempfile
import unittest

from autopom.extraction.schema import ActionModel, ElementModel, PageModel, SectionModel
from autopom.generation.java_generator import JavaGenerator, JavaGeneratorConfig


class TestJavaGenerator(unittest.TestCase):
    def _sample_page(self) -> PageModel:
        return PageModel(
            page_id="login",
            page_name="LoginPage",
            url="https://example.com/login",
            route="/login",
            sections=[
                SectionModel(
                    name="mainContent",
                    elements=[
                        ElementModel(
                            element_id="usernameInput",
                            type="input",
                            role="textbox",
                            semantic_label="Username",
                            selector="input[name='username']",
                        ),
                        ElementModel(
                            element_id="signInButton",
                            type="button",
                            role="button",
                            semantic_label="Sign In",
                            selector="button:has-text(\"Sign In\")",
                        ),
                    ],
                )
            ],
            actions=[
                ActionModel(
                    name="login",
                    params=["username"],
                    steps=["fill(usernameInput, username)", "click(signInButton)"],
                    post_condition="dashboardLoaded",
                )
            ],
        )

    def test_generates_base_and_page_java_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            generator = JavaGenerator(
                output_dir=output_dir,
                template_dir=Path("unused-in-current-generator"),
                config=JavaGeneratorConfig(base_package="com.example.autopom"),
            )
            base_path = generator.generate_base_page()
            page_path = generator.generate_page(self._sample_page())

            self.assertTrue(base_path.exists())
            self.assertTrue(page_path.exists())

            page_content = page_path.read_text(encoding="utf-8")
            self.assertIn("package com.example.autopom.pages;", page_content)
            self.assertIn("private final Locator usernameInput;", page_content)
            self.assertIn('this.signInButton = locator("button:has-text(\\"Sign In\\")");', page_content)
            self.assertIn("public LoginPage login(String username)", page_content)
            self.assertIn("signInButton.click();", page_content)


if __name__ == "__main__":
    unittest.main()
