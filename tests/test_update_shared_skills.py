from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import update_shared_skills
from test_sync_skills import write_skill

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
UPDATE_SCRIPT = SCRIPTS / "update_shared_skills.py"
SYNC_SCRIPT = SCRIPTS / "sync_skills.py"


def run(*command: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)


class UpdateSharedSkillsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        base = Path(self.temporary_directory.name)
        self.source = base / "source"
        self.target = base / "target"
        for root in (self.source, self.target):
            (root / ".agents" / "skills").mkdir(parents=True)
            (root / ".claude" / "skills").mkdir(parents=True)
            (root / "scripts").mkdir()
            (root / "scripts" / "sync_skills.py").write_text(
                SYNC_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8"
            )
            (root / "scripts" / "update_shared_skills.py").write_text(
                UPDATE_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8"
            )

        # Source: one shared skill with a reference file, one local-only skill.
        shared = write_skill(self.source, name="shared-skill", origin="shared")
        (shared.parent / "references").mkdir()
        (shared.parent / "references" / "guide.md").write_text("v2\n", encoding="utf-8")
        write_skill(self.source, name="source-local", origin="local")
        (self.source / "_notes" / "grills").mkdir(parents=True)
        (self.source / "_notes" / "README.md").write_text("# notes\n", encoding="utf-8")
        (self.source / "_notes" / "grills" / "README.md").write_text("# grills\n", encoding="utf-8")
        self.assertEqual(self.run_sync(self.source).returncode, 0)

    def run_sync(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return run(
            sys.executable,
            str(root / "scripts" / "sync_skills.py"),
            "--root",
            str(root),
            *arguments,
        )

    def run_update(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return run(
            sys.executable,
            str(self.target / "scripts" / "update_shared_skills.py"),
            "--root",
            str(self.target),
            "--source",
            str(self.source),
            *arguments,
        )

    def test_update_copies_shared_skills_and_scaffold_but_not_local(self) -> None:
        write_skill(self.target, name="target-local", origin="local")
        stale = write_skill(self.target, name="shared-skill", origin="shared")
        (stale.parent / "references").mkdir()
        (stale.parent / "references" / "guide.md").write_text("v1\n", encoding="utf-8")
        (stale.parent / "references" / "obsolete.md").write_text("gone\n", encoding="utf-8")
        venv = stale.parent / "scripts" / ".venv"
        venv.mkdir(parents=True)
        (venv / "pyvenv.cfg").write_text("keep\n", encoding="utf-8")

        result = self.run_update()

        self.assertEqual(result.returncode, 0, result.stderr)
        skills = self.target / ".agents" / "skills"
        self.assertEqual(
            (skills / "shared-skill/references/guide.md").read_text(encoding="utf-8"), "v2\n"
        )
        self.assertFalse((skills / "shared-skill/references/obsolete.md").exists())
        self.assertTrue((venv / "pyvenv.cfg").is_file())
        self.assertFalse((skills / "source-local").exists())
        self.assertTrue((skills / "target-local" / "SKILL.md").is_file())
        self.assertTrue((self.target / "_notes" / "grills" / "README.md").is_file())
        self.assertTrue(
            (self.target / ".claude" / "skills" / "shared-skill" / "SKILL.md").is_file()
        )

        lock = json.loads((self.target / ".agents" / "skills.lock").read_text(encoding="utf-8"))
        self.assertEqual(lock["shared_source"]["url"], str(self.source))
        self.assertIn("shared-skill", lock["skills"])
        self.assertIn("target-local", lock["skills"])
        self.assertEqual(self.run_sync(self.target, "--check").returncode, 0)

    def test_update_does_not_overwrite_existing_scaffold(self) -> None:
        (self.target / "_notes").mkdir()
        (self.target / "_notes" / "README.md").write_text("custom\n", encoding="utf-8")

        self.assertEqual(self.run_update().returncode, 0)

        self.assertEqual(
            (self.target / "_notes" / "README.md").read_text(encoding="utf-8"), "custom\n"
        )

    def test_update_refuses_local_skill_that_collides_with_shared_name(self) -> None:
        write_skill(self.target, name="shared-skill", origin="local")

        result = self.run_update()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("collide with shared skill names: shared-skill", result.stderr)
        self.assertFalse(
            (self.target / ".agents" / "skills" / "shared-skill" / "references").exists()
        )

    def test_dry_run_writes_nothing(self) -> None:
        result = self.run_update("--dry-run")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("would write", result.stdout)
        self.assertFalse((self.target / ".agents" / "skills" / "shared-skill").exists())
        self.assertFalse((self.target / ".agents" / "skills.lock").exists())

    def test_update_warns_about_orphaned_shared_skill(self) -> None:
        write_skill(self.target, name="retired", origin="shared")

        result = self.run_update()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("shared skill 'retired' no longer exists in the source", result.stderr)
        self.assertTrue((self.target / ".agents" / "skills" / "retired" / "SKILL.md").is_file())

    def test_update_clones_git_source_at_ref(self) -> None:
        if run("git", "--version").returncode != 0:
            self.skipTest("git is not available")
        run("git", "init", "-q", cwd=self.source)
        run(
            "git",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "add",
            ".",
            cwd=self.source,
        )
        commit = run(
            "git",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "commit",
            "-q",
            "-m",
            "init",
            cwd=self.source,
        )
        self.assertEqual(commit.returncode, 0, commit.stderr)
        run("git", "tag", "v1.0.0", cwd=self.source)

        result = run(
            sys.executable,
            str(self.target / "scripts" / "update_shared_skills.py"),
            "--root",
            str(self.target),
            "--source",
            self.source.as_uri(),
            "--ref",
            "v1.0.0",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        lock = json.loads((self.target / ".agents" / "skills.lock").read_text(encoding="utf-8"))
        self.assertEqual(lock["shared_source"]["ref"], "v1.0.0")
        self.assertEqual(len(lock["shared_source"]["commit"]), 40)

    def snapshot(self) -> dict[str, bytes]:
        return {
            str(path.relative_to(self.target)): path.read_bytes()
            for path in self.target.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }

    def test_new_sync_version_is_used_on_first_update(self) -> None:
        script = self.source / "scripts/sync_skills.py"
        script.write_text(
            script.read_text(encoding="utf-8").replace('"# Skill catalog"', '"# Skill catalog v2"'),
            encoding="utf-8",
        )
        result = self.run_update()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Skill catalog v2", (self.target / ".agents/skills/CATALOG.md").read_text())
        result = self.run_sync(self.target, "--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_failed_new_sync_leaves_target_unchanged(self) -> None:
        (self.source / "scripts/sync_skills.py").write_text(
            "raise SystemExit(17)\n", encoding="utf-8"
        )
        before = self.snapshot()
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("staged sync failed", result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_manual_adapter_failure_leaves_shared_files_and_lock_unchanged(self) -> None:
        skill = write_skill(self.target, name="shared-skill")
        refs = skill.parent / "references"
        refs.mkdir()
        (refs / "guide.md").write_text("v1", encoding="utf-8")
        (refs / "obsolete.md").write_text("keep on failure", encoding="utf-8")
        self.assertEqual(self.run_sync(self.target).returncode, 0)
        manual = self.target / ".claude/skills/manual/SKILL.md"
        manual.parent.mkdir()
        manual.write_text("manual", encoding="utf-8")
        before = self.snapshot()
        for arguments in ((), ("--dry-run",)):
            result = self.run_update(*arguments)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unmanaged", result.stderr)
            self.assertEqual(self.snapshot(), before)

    def test_malformed_lock_fails_before_any_update(self) -> None:
        (self.target / ".agents/skills.lock").write_text("{broken", encoding="utf-8")
        before = self.snapshot()
        result = self.run_update()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_png_asset_copied_and_updated(self) -> None:
        source = self.source / ".agents/skills/shared-skill/assets/logo.png"
        source.parent.mkdir()
        source.write_bytes(b"\x89PNG\r\nversion-1")
        generated = source.parent / "_generated"
        generated.mkdir()
        (generated / "preview.png").write_bytes(b"preview")
        for content in (b"\x89PNG\r\nversion-1", b"\x89PNG\r\nversion-2"):
            source.write_bytes(content)
            result = self.run_update()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((self.target / source.relative_to(self.source)).read_bytes(), content)
            self.assertFalse((self.target / generated.relative_to(self.source)).exists())
            self.assertEqual(self.run_sync(self.target, "--check").returncode, 0)

    def test_source_and_target_directory_links_fail_without_external_write(self) -> None:
        write_skill(self.target, name="shared-skill")
        with tempfile.TemporaryDirectory() as temporary:
            external = Path(temporary)
            sentinel = external / "guide.md"
            sentinel.write_bytes(b"keep me")
            for root in (self.target, self.source):
                link = root / ".agents/skills/shared-skill/references"
                if link.exists():
                    shutil.rmtree(link)
                try:
                    link.symlink_to(external, target_is_directory=True)
                except OSError as error:
                    self.skipTest(f"directory symlink unavailable: {error}")
                before = self.snapshot()
                result = self.run_update()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("symlinks", result.stderr)
                self.assertEqual(sentinel.read_bytes(), b"keep me")
                self.assertEqual(self.snapshot(), before)
                link.unlink()

    def test_tooling_parent_link_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            external = Path(temporary)
            link = self.target / "tests"
            try:
                link.symlink_to(external, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error}")
            result = self.run_update()
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlinks", result.stderr)
            self.assertEqual(list(external.iterdir()), [])

    def test_dry_run_preserves_all_target_bytes(self) -> None:
        before = self.snapshot()
        result = self.run_update("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_commit_write_failure_rolls_back_whole_update(self) -> None:
        skill = write_skill(self.target, name="shared-skill")
        (skill.parent / "obsolete.md").write_text("restore me", encoding="utf-8")
        self.assertEqual(self.run_sync(self.target).returncode, 0)
        before = self.snapshot()
        real_write = update_shared_skills.sync_skills.atomic_write_bytes
        fail_path = self.target / ".agents/skills/shared-skill/references/guide.md"
        failed = False

        def fail_once(path, content):
            nonlocal failed
            if path == fail_path and not failed:
                failed = True
                raise OSError("injected commit failure")
            return real_write(path, content)

        with mock.patch.object(
            update_shared_skills.sync_skills, "atomic_write_bytes", side_effect=fail_once
        ):
            with self.assertRaisesRegex(OSError, "injected commit failure"):
                update_shared_skills.update(self.target, str(self.source), "main", False)
        self.assertTrue(failed)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
