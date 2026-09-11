from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / "scripts" / "bootstrap_template.py"
sys.path.insert(0, str(SCRIPT.parent))
import bootstrap_template

COPIED = (
    "pyproject.toml",
    "README.md",
    "AGENTS.md",
    "src/project_template/__init__.py",
    "tests/test_project_template.py",
    "scripts/bootstrap_template.py",
    "tests/test_bootstrap_template.py",
)


class BootstrapTemplateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        for relative in COPIED:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPOSITORY_ROOT / relative, target)
        (self.root / "uv.lock").write_text(
            '[[package]]\nname = "project-template"\nsource = { editable = "." }\n',
            encoding="utf-8",
        )

    def run_script(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), "--no-lock", *arguments],
            capture_output=True,
            text=True,
        )

    def read(self, relative: str) -> str:
        return (self.root / relative).read_text(encoding="utf-8")

    def test_bootstrap_renames_package_and_replaces_placeholders(self) -> None:
        result = self.run_script("my-project", "--description", "Does things.")
        self.assertEqual(result.returncode, 0, result.stderr)

        self.assertTrue((self.root / "src" / "my_project" / "__init__.py").is_file())
        self.assertFalse((self.root / "src" / "project_template").exists())
        self.assertTrue((self.root / "tests" / "test_my_project.py").is_file())
        self.assertIn("import my_project", self.read("tests/test_my_project.py"))

        pyproject = self.read("pyproject.toml")
        self.assertIn('name = "my-project"', pyproject)
        self.assertIn('description = "Does things."', pyproject)
        self.assertIn('packages = ["src/my_project"]', pyproject)
        self.assertIn('name = "my-project"', self.read("uv.lock"))

        readme = self.read("README.md")
        self.assertNotIn("template-only", readme)
        self.assertNotIn("project-template", readme)
        self.assertNotIn("project_template", readme)
        self.assertTrue(readme.startswith("# my-project\n"))

        for relative in ("scripts/bootstrap_template.py", "tests/test_bootstrap_template.py"):
            self.assertFalse((self.root / relative).exists(), relative)

    def test_keep_script_and_explicit_package(self) -> None:
        result = self.run_script("my-project", "--package", "core", "--keep-script")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "src" / "core" / "__init__.py").is_file())
        self.assertTrue((self.root / "scripts" / "bootstrap_template.py").is_file())
        self.assertIn('packages = ["src/core"]', self.read("pyproject.toml"))

    def test_second_run_is_rejected(self) -> None:
        self.assertEqual(self.run_script("my-project", "--keep-script").returncode, 0)
        result = self.run_script("other-project")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already bootstrapped", result.stderr)
        self.assertTrue((self.root / "src" / "my_project").is_dir())

    def test_invalid_names_are_rejected_before_changing_files(self) -> None:
        for arguments in (["My_Project"], ["my--project"], ["ok-name", "--package", "class"]):
            with self.subTest(arguments=arguments):
                result = self.run_script(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("invalid", result.stderr)
                self.assertTrue((self.root / "src" / "project_template").is_dir())

    def test_template_block_regex_removes_only_marked_section(self) -> None:
        text = (
            "# title\n\n<!-- template-only:start -->\nguide\n<!-- template-only:end -->\n\nrest\n"
        )
        self.assertEqual(bootstrap_template.TEMPLATE_BLOCK.sub("", text), "# title\n\nrest\n")


if __name__ == "__main__":
    unittest.main()
