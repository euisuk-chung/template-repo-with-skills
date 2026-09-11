#!/usr/bin/env python3
"""Turn a fresh copy of the template into a named project.

Run once right after creating a repository from the template::

    python3 scripts/bootstrap_template.py my-project
    python3 scripts/bootstrap_template.py my-project --package mypkg --description "..."

The script renames the placeholder package, replaces the ``project-template`` /
``project_template`` placeholders in the project files, removes the template-only
section from the README, refreshes ``uv.lock`` when ``uv`` is available, and then
deletes itself together with its tests. Shared skills and the skill tooling are not
touched; refresh those with ``scripts/update_shared_skills.py``.
"""

from __future__ import annotations

import argparse
import keyword
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER_NAME = "project-template"
PLACEHOLDER_PACKAGE = "project_template"
PLACEHOLDER_DESCRIPTION = "Project description."
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PACKAGE_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*$")
TEMPLATE_BLOCK = re.compile(
    r"^<!-- template-only:start -->\n.*?^<!-- template-only:end -->\n\n?",
    re.DOTALL | re.MULTILINE,
)
# Files that carry the placeholders. Missing files are skipped.
PLACEHOLDER_FILES = ("pyproject.toml", "uv.lock", "README.md", "AGENTS.md")
SELF_FILES = ("scripts/bootstrap_template.py", "tests/test_bootstrap_template.py")


class BootstrapError(RuntimeError):
    """Raised when the repository cannot be bootstrapped safely."""


def validate(name: str, package: str) -> None:
    if not NAME_PATTERN.fullmatch(name):
        raise BootstrapError(
            f"invalid project name {name!r}: use lowercase letters, digits and single hyphens"
        )
    if not PACKAGE_PATTERN.fullmatch(package) or keyword.iskeyword(package):
        raise BootstrapError(f"invalid package name {package!r}: use a lowercase Python identifier")
    if package == PLACEHOLDER_PACKAGE or name == PLACEHOLDER_NAME:
        raise BootstrapError("choose a name other than the placeholder")


def replace_placeholders(text: str, name: str, package: str, description: str) -> str:
    text = text.replace(
        f'description = "{PLACEHOLDER_DESCRIPTION}"', f'description = "{description}"'
    )
    text = text.replace(PLACEHOLDER_DESCRIPTION, description)
    text = text.replace(PLACEHOLDER_PACKAGE, package)
    return text.replace(PLACEHOLDER_NAME, name)


def rewrite(path: Path, transform) -> None:
    original = path.read_text(encoding="utf-8")
    updated = transform(original)
    if updated != original:
        path.write_text(updated, encoding="utf-8", newline="\n")


def bootstrap(
    root: Path,
    name: str,
    package: str,
    description: str,
    *,
    keep_script: bool = False,
    lock: bool = True,
) -> list[str]:
    """Apply the bootstrap and return a human-readable list of what changed."""
    validate(name, package)
    package_dir = root / "src" / PLACEHOLDER_PACKAGE
    if not package_dir.is_dir():
        raise BootstrapError(
            f"{package_dir.relative_to(root)} is missing; the repository is already bootstrapped"
        )
    target_dir = root / "src" / package
    if target_dir.exists():
        raise BootstrapError(f"{target_dir.relative_to(root)} already exists")

    changes: list[str] = []
    package_dir.rename(target_dir)
    changes.append(f"renamed src/{PLACEHOLDER_PACKAGE} -> src/{package}")

    old_test = root / "tests" / f"test_{PLACEHOLDER_PACKAGE}.py"
    new_test = root / "tests" / f"test_{package}.py"
    if old_test.is_file() and not new_test.exists():
        old_test.rename(new_test)
        changes.append(f"renamed tests/{old_test.name} -> tests/{new_test.name}")

    def substitute(text: str) -> str:
        return replace_placeholders(text, name, package, description)

    for relative in (
        *PLACEHOLDER_FILES,
        f"src/{package}/__init__.py",
        f"tests/{new_test.name}",
    ):
        path = root / relative
        if path.is_file():
            rewrite(path, substitute)
            changes.append(f"updated {relative}")

    readme = root / "README.md"
    if readme.is_file():
        rewrite(readme, lambda text: TEMPLATE_BLOCK.sub("", text))
        changes.append("removed the template-only section from README.md")

    if lock and (root / "uv.lock").is_file():
        uv = shutil.which("uv")
        if uv:
            subprocess.run([uv, "lock"], cwd=root, check=True)
            changes.append("refreshed uv.lock")
        else:
            changes.append("uv not found: run `uv lock` to refresh uv.lock")

    if not keep_script:
        for relative in SELF_FILES:
            path = root / relative
            if path.is_file():
                path.unlink()
                changes.append(f"deleted {relative}")
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("name", help="project name for pyproject.toml, e.g. my-project")
    parser.add_argument("--package", help="import package name (default: name with '_')")
    parser.add_argument("--description", default=PLACEHOLDER_DESCRIPTION)
    parser.add_argument("--keep-script", action="store_true", help="do not delete this script")
    parser.add_argument("--no-lock", action="store_true", help="skip running `uv lock`")
    parser.add_argument(
        "--root", type=Path, default=DEFAULT_REPOSITORY_ROOT, help=argparse.SUPPRESS
    )
    args = parser.parse_args()
    package = args.package or args.name.replace("-", "_")
    try:
        changes = bootstrap(
            args.root.resolve(),
            args.name,
            package,
            args.description,
            keep_script=args.keep_script,
            lock=not args.no_lock,
        )
    except (BootstrapError, OSError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    for change in changes:
        print(change)
    print("\nNext: review `git diff`, then run `uv sync` and `uv run pre-commit install`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
