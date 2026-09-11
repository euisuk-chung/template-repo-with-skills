from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_skills.py"
sys.path.insert(0, str(SCRIPT.parent))
import sync_skills


def write_skill(
    root: Path,
    name: str = "example-skill",
    description: str = "Use for portable adapter tests.",
    group: str = "test",
    origin: str = "shared",
    extra_frontmatter: list[str] | None = None,
) -> Path:
    skill_directory = root / ".agents" / "skills" / name
    skill_directory.mkdir(parents=True)
    skill_file = skill_directory / "SKILL.md"
    skill_file.write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                f'description: "{description}"',
                *(extra_frontmatter or []),
                "metadata:",
                f"  group: {group}",
                f"  origin: {origin}",
                "---",
                "",
                "# Instructions",
                "",
                "Follow the test workflow.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    return skill_file


class SyncSkillsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        (self.root / ".agents" / "skills").mkdir(parents=True)
        (self.root / ".claude" / "skills").mkdir(parents=True)

    def run_sync(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def write_skill(self, **kwargs) -> Path:
        return write_skill(self.root, **kwargs)

    def adapter(self, name: str = "example-skill") -> Path:
        return self.root / ".claude" / "skills" / name / "SKILL.md"

    def lock(self) -> dict:
        return json.loads((self.root / ".agents" / "skills.lock").read_text(encoding="utf-8"))

    def test_empty_skillset_is_valid_after_sync(self) -> None:
        self.assertEqual(self.run_sync().returncode, 0)
        result = self.run_sync("--check")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("0 skill(s)", result.stdout)
        self.assertIn(
            "No skills are defined yet.", (self.root / ".agents/skills/CATALOG.md").read_text()
        )

    def test_sync_generates_adapter_catalog_and_lock(self) -> None:
        self.write_skill(
            extra_frontmatter=['argument-hint: "topic"', "disable-model-invocation: true"]
        )

        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)

        content = self.adapter().read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: example-skill\n"))
        self.assertIn('argument-hint: "topic"\ndisable-model-invocation: true', content)
        self.assertIn("metadata:\n  group: test\n  origin: shared", content)
        self.assertIn("`.agents/skills/example-skill/SKILL.md`", content)
        self.assertNotIn("../", content)
        self.assertNotIn("\\", content)

        catalog = (self.root / ".agents" / "skills" / "CATALOG.md").read_text(encoding="utf-8")
        self.assertIn("## test", catalog)
        self.assertIn("[`example-skill`](example-skill/SKILL.md) | shared |", catalog)

        lock = self.lock()
        self.assertEqual(lock["skills"]["example-skill"]["origin"], "shared")
        self.assertEqual(lock["skills"]["example-skill"]["group"], "test")
        self.assertEqual(len(lock["skills"]["example-skill"]["sha256"]), 64)
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_multiline_description_is_supported(self) -> None:
        skill_directory = self.root / ".agents" / "skills" / "block-description"
        skill_directory.mkdir(parents=True)
        (skill_directory / "SKILL.md").write_text(
            "---\n"
            "name: block-description\n"
            "description: >-\n"
            "  Use when a description needs more than one line and should remain\n"
            "  portable across the shared harnesses.\n"
            "metadata:\n"
            "  group: test\n"
            "  origin: local\n"
            "---\n\n"
            "# Instructions\n\nFollow them.\n",
            encoding="utf-8",
            newline="\n",
        )

        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "description: >-\n", self.adapter("block-description").read_text(encoding="utf-8")
        )
        catalog = (self.root / ".agents" / "skills" / "CATALOG.md").read_text(encoding="utf-8")
        self.assertIn("more than one line and should remain portable", catalog)
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_check_detects_and_sync_repairs_modified_generated_adapter(self) -> None:
        self.write_skill()
        self.assertEqual(self.run_sync().returncode, 0)
        adapter = self.adapter()
        adapter.write_text(
            adapter.read_text(encoding="utf-8") + "manual change\n", encoding="utf-8"
        )

        check_result = self.run_sync("--check")
        self.assertNotEqual(check_result.returncode, 0)
        self.assertIn("outdated adapter", check_result.stderr)

        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_check_detects_drift_in_shared_and_local_skills(self) -> None:
        shared = self.write_skill(name="shared-skill", origin="shared")
        local = self.write_skill(name="local-skill", origin="local")
        self.assertEqual(self.run_sync().returncode, 0)

        shared.write_text(shared.read_text(encoding="utf-8") + "\nMore.\n", encoding="utf-8")
        result = self.run_sync("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("shared skill differs from lock file: shared-skill", result.stderr)
        self.assertIn("update_shared_skills.py", result.stderr)

        self.assertEqual(self.run_sync().returncode, 0)
        local.write_text(local.read_text(encoding="utf-8") + "\nMore.\n", encoding="utf-8")
        result = self.run_sync("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("local skill differs from lock file: local-skill", result.stderr)

    def test_hash_ignores_local_environment_files(self) -> None:
        skill_file = self.write_skill()
        self.assertEqual(self.run_sync().returncode, 0)
        before = self.lock()["skills"]["example-skill"]["sha256"]

        venv = skill_file.parent / "scripts" / ".venv"
        venv.mkdir(parents=True)
        (venv / "pyvenv.cfg").write_text("home = /usr/bin\n", encoding="utf-8")
        previews = skill_file.parent / "_generated"
        previews.mkdir()
        (previews / "preview.png").write_bytes(b"\x89PNG")

        self.assertEqual(self.run_sync("--check").returncode, 0)
        self.assertEqual(self.lock()["skills"]["example-skill"]["sha256"], before)

    def test_sync_preserves_shared_source_in_lock(self) -> None:
        self.write_skill()
        self.assertEqual(self.run_sync().returncode, 0)
        lock_path = self.root / ".agents" / "skills.lock"
        lock = self.lock()
        lock["shared_source"] = {
            "url": "https://example.invalid/t.git",
            "ref": "v1",
            "commit": "abc",
        }
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(self.lock()["shared_source"]["ref"], "v1")

    def test_sync_removes_only_stale_generated_adapter(self) -> None:
        skill_file = self.write_skill()
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertTrue(self.adapter().is_file())

        shutil.rmtree(skill_file.parent)
        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.adapter().exists())
        self.assertNotIn("example-skill", self.lock()["skills"])

    def test_sync_refuses_to_overwrite_unmanaged_claude_skill(self) -> None:
        manual = self.root / ".claude" / "skills" / "manual" / "SKILL.md"
        manual.parent.mkdir(parents=True)
        original = "---\nname: manual\ndescription: Manual file.\n---\nKeep me.\n"
        manual.write_text(original, encoding="utf-8")

        result = self.run_sync()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("refusing to overwrite unmanaged file", result.stderr)
        self.assertEqual(manual.read_text(encoding="utf-8"), original)

    def test_invalid_name_fails_before_writing(self) -> None:
        skill_file = self.write_skill()
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace(
                "name: example-skill", "name: Different_Name"
            ),
            encoding="utf-8",
        )

        result = self.run_sync()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lowercase letters, digits, and hyphens", result.stderr)
        self.assertEqual(list((self.root / ".claude" / "skills").glob("*/SKILL.md")), [])

    def test_missing_metadata_is_rejected(self) -> None:
        skill_directory = self.root / ".agents" / "skills" / "bare"
        skill_directory.mkdir(parents=True)
        (skill_directory / "SKILL.md").write_text(
            "---\nname: bare\ndescription: Bare.\n---\n\nBody.\n", encoding="utf-8"
        )

        result = self.run_sync()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing frontmatter field(s): metadata", result.stderr)

    def test_invalid_origin_and_unknown_field_are_rejected(self) -> None:
        self.write_skill(name="bad-origin", origin="upstream")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata.origin must be one of", result.stderr)

        shutil.rmtree(self.root / ".agents" / "skills" / "bad-origin")
        self.write_skill(name="bad-field", extra_frontmatter=["hooks: none"])
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported frontmatter field 'hooks'", result.stderr)

    def test_korean_description_is_rejected(self) -> None:
        self.write_skill(description="한국어 설명은 허용하지 않는다.")

        result = self.run_sync()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("description must be written in English", result.stderr)

    def test_check_validates_note_filenames(self) -> None:
        self.write_skill()
        self.assertEqual(self.run_sync().returncode, 0)
        grills = self.root / "_notes" / "grills"
        grills.mkdir(parents=True)
        (grills / "README.md").write_text("# grills\n", encoding="utf-8")
        (grills / "260908-1500-search-filter.md").write_text("ok\n", encoding="utf-8")
        self.assertEqual(self.run_sync("--check").returncode, 0)

        (grills / "search-filter.md").write_text("bad\n", encoding="utf-8")
        result = self.run_sync("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("note filename must match", result.stderr)

    def test_invalid_yaml_fails_before_generating(self) -> None:
        skill = self.write_skill()
        original = skill.read_text(encoding="utf-8")
        cases = [
            original.replace('"Use for portable adapter tests."', "Review: changes"),
            original.replace('"Use for portable adapter tests."', "123"),
            original.replace('"Use for portable adapter tests."', "[one, two]"),
            original.replace('"Use for portable adapter tests."', "null"),
            original.replace('"Use for portable adapter tests."', "*alias"),
            original.replace('"Use for portable adapter tests."', '"quoted"#bad-comment'),
            original.replace("  origin: shared", "    origin: shared"),
            original.replace("metadata:", "  stray: value\nmetadata:"),
            original.replace("metadata:", "allowed-tools: [Read, Bash]\nmetadata:"),
            original.replace("metadata:", 'disable-model-invocation: "true"\nmetadata:'),
            original.replace("metadata:", "model: broken: value\nmetadata:"),
            original.replace("  group:", "\tgroup:"),
            original.replace("description: ", "description:"),
            original.replace("metadata:", "metadata:#bad-comment"),
            original.replace("  origin: shared", "  origin:shared"),
            original.replace("  origin: shared", "  origin: shared\n  true: value"),
        ]
        for content in cases:
            with self.subTest(content=content):
                skill.write_text(content, encoding="utf-8")
                result = self.run_sync()
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertFalse(self.adapter().exists())

    def test_quoted_colon_and_metadata_comments_are_supported(self) -> None:
        skill = self.write_skill(description="Review: changes")
        skill.write_text(
            skill.read_text(encoding="utf-8").replace("  origin:", "  # ownership\n  origin:"),
            encoding="utf-8",
        )
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_png_assets_are_hashed_but_generated_previews_are_not(self) -> None:
        skill = self.write_skill()
        assets = skill.parent / "assets"
        assets.mkdir()
        logo = assets / "logo.png"
        logo.write_bytes(b"\x89PNG\r\nversion-1")
        self.assertEqual(self.run_sync().returncode, 0)
        before = sync_skills.skill_content_hash(skill.parent)
        logo.write_bytes(b"\x89PNG\nversion-1")
        self.assertNotEqual(before, sync_skills.skill_content_hash(skill.parent))
        self.assertNotEqual(self.run_sync("--check").returncode, 0)

    def test_text_hash_normalizes_only_known_text_formats(self) -> None:
        skill = self.write_skill()
        for name in ("config.toml", "uv.lock", "template.html", "data.json"):
            file = skill.parent / name
            file.write_bytes(b"first\nsecond\n")
            before = sync_skills.skill_content_hash(skill.parent)
            file.write_bytes(b"first\r\nsecond\r\n")
            self.assertEqual(before, sync_skills.skill_content_hash(skill.parent))
        unknown = skill.parent / "unknown.bin"
        unknown.write_bytes(b"first\n")
        before = sync_skills.skill_content_hash(skill.parent)
        unknown.write_bytes(b"first\r\n")
        self.assertNotEqual(before, sync_skills.skill_content_hash(skill.parent))

    def test_skill_file_order_and_hash_are_platform_independent(self) -> None:
        skill = write_skill(self.root)
        references = skill.parent / "references"
        references.mkdir()
        (references / "notes.md").write_text("reference\n", encoding="utf-8")
        (skill.parent / "Zeta.txt").write_text("asset\n", encoding="utf-8")

        ordered = [path.as_posix() for path in sync_skills.iter_skill_files(skill.parent)]
        # Byte order: uppercase names sort before lowercase, regardless of the host
        # filesystem or of pathlib's case-insensitive comparison on Windows.
        self.assertEqual(ordered, ["SKILL.md", "Zeta.txt", "references/notes.md"])

        digest = sync_skills.skill_content_hash(skill.parent)
        with mock.patch.object(
            sync_skills.Path, "__lt__", lambda self, other: str(self).lower() < str(other).lower()
        ):
            self.assertEqual(digest, sync_skills.skill_content_hash(skill.parent))

    def test_git_autocrlf_checkout_passes_check(self) -> None:
        skill = self.write_skill()
        (skill.parent / "config.toml").write_bytes(b'name = "test"\n')
        # Simulate a downstream checkout without LF rules for every text format.
        # Keep the test independent of downstream-owned repository configuration.
        (self.root / ".gitattributes").write_bytes(b"* text=auto\n*.md text eol=lf\n")
        self.assertEqual(self.run_sync().returncode, 0)
        commands = [
            ["git", "init", "-q"],
            ["git", "config", "core.autocrlf", "false"],
            ["git", "add", "."],
            [
                "git",
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@example.invalid",
                "commit",
                "-qm",
                "fixture",
            ],
        ]
        for command in commands:
            result = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        with tempfile.TemporaryDirectory() as temporary:
            clone = Path(temporary) / "checkout"
            result = subprocess.run(
                [
                    "git",
                    "clone",
                    "-q",
                    "--no-hardlinks",
                    "-c",
                    "core.autocrlf=true",
                    str(self.root),
                    str(clone),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                b"\r\n",
                (clone / skill.relative_to(self.root)).with_name("config.toml").read_bytes(),
            )
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(clone), "--check"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_lock_does_not_delete_stale_adapter(self) -> None:
        skill = self.write_skill()
        self.assertEqual(self.run_sync().returncode, 0)
        original = self.adapter().read_bytes()
        shutil.rmtree(skill.parent)
        (self.root / ".agents/skills.lock").write_text("{broken", encoding="utf-8")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.adapter().read_bytes(), original)

    def test_directory_symlink_is_rejected_and_ignored_environment_is_pruned(self) -> None:
        skill = self.write_skill()
        with tempfile.TemporaryDirectory() as temporary:
            external = Path(temporary)
            link = skill.parent / "references"
            try:
                link.symlink_to(external, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")
            result = self.run_sync()
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlinks", result.stderr)
            link.unlink()
            (skill.parent / ".venv").symlink_to(external, target_is_directory=True)
            # A non-regular entry proves the ignored environment was not traversed.
            (external / "nested-link").symlink_to(external, target_is_directory=True)
            self.assertEqual(self.run_sync().returncode, 0)

    def test_atomic_batch_restores_deleted_and_overwritten_files(self) -> None:
        first, second = self.root / "first", self.root / "second"
        first.write_bytes(b"original first")
        first.chmod(0o755)
        original_mode = first.stat().st_mode
        second.write_bytes(b"original second")
        new = self.root / "new-directory/new-file"
        original_write = sync_skills.atomic_write_bytes
        failed = False

        def fail_once(path, content):
            nonlocal failed
            if path == new and not failed:
                failed = True
                raise OSError("injected write failure")
            return original_write(path, content)

        with mock.patch.object(sync_skills, "atomic_write_bytes", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "injected"):
                sync_skills.apply_changes(self.root, {first: None, second: b"new", new: b"new"})
        self.assertEqual(first.read_bytes(), b"original first")
        self.assertEqual(first.stat().st_mode, original_mode)
        self.assertEqual(second.read_bytes(), b"original second")
        self.assertFalse(new.parent.exists())


if __name__ == "__main__":
    unittest.main()
