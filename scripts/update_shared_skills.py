#!/usr/bin/env python3
"""Refresh shared skills and skill tooling from the template repository.

Downstream repositories created from the template run this script to pull the
current ``origin: shared`` skills, the skill tooling (this script, the sync script,
their tests, and the CI workflow), and the ``_notes`` scaffold READMEs when they are
missing. Skills with ``origin: local`` are never touched. After copying, the sync
script regenerates the Claude adapters, catalog, and lock file.

Examples::

    python3 scripts/update_shared_skills.py --ref v1.2.0
    python3 scripts/update_shared_skills.py --source ../template-repo-with-skills
    python3 scripts/update_shared_skills.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True

import sync_skills  # noqa: E402

DEFAULT_SOURCE = "https://github.com/euisuk-chung/template-repo-with-skills.git"
DEFAULT_REF = "main"

# Files copied verbatim from the source on every update.
SHARED_TOOLING = (
    "scripts/sync_skills.py",
    "scripts/update_shared_skills.py",
    "tests/test_sync_skills.py",
    "tests/test_update_shared_skills.py",
    ".github/workflows/validate-skills.yml",
    ".agents/skills/README.md",
    ".claude/skills/README.md",
)

# Files copied only when they do not exist yet, so repositories can customise them.
SCAFFOLD_IF_MISSING = (
    "_notes/README.md",
    "_notes/grills/README.md",
    "_notes/handoffs/README.md",
    "_notes/handoffs/to_codex/README.md",
    "_notes/handoffs/to_claude/README.md",
    "_notes/handoffs/to_human/README.md",
)


class UpdateError(RuntimeError):
    """Raised when the update cannot proceed safely."""


def git(*arguments: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise UpdateError(f"git {' '.join(arguments)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def resolve_source(source: str, ref: str, workdir: Path) -> tuple[Path, str | None]:
    """Return a checkout directory for the source and its commit, if known."""
    candidate = Path(source).expanduser()
    if candidate.is_dir():
        root = candidate.resolve()
        try:
            commit = git("rev-parse", "HEAD", cwd=root)
        except UpdateError:
            commit = None
        return root, commit

    checkout = workdir / "source"
    git("clone", "--quiet", "--depth", "1", "--branch", ref, source, str(checkout))
    return checkout, git("rev-parse", "HEAD", cwd=checkout)


def copy_skill_directory(source: Path, destination: Path, dry_run: bool) -> list[str]:
    """Mirror a skill directory, leaving hash-ignored local content alone."""
    actions: list[str] = []
    source_files = set(sync_skills.iter_skill_files(source))
    destination_files = (
        set(sync_skills.iter_skill_files(destination)) if destination.is_dir() else set()
    )

    for relative in sorted(source_files):
        source_file = source / relative
        destination_file = destination / relative
        sync_skills.safe_path(source, source_file)
        sync_skills.safe_path(destination, destination_file)
        if destination_file.is_file() and destination_file.read_bytes() == source_file.read_bytes():
            continue
        actions.append(f"write {destination_file}")
        if not dry_run:
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_file, destination_file)

    for relative in sorted(destination_files - source_files):
        stale = destination / relative
        actions.append(f"delete {stale}")
        if not dry_run:
            stale.unlink()
            parent = stale.parent
            while parent != destination and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
    return actions


def copy_file(source: Path, destination: Path, dry_run: bool) -> bool:
    if not source.is_file():
        return False
    if destination.is_file() and destination.read_bytes() == source.read_bytes():
        return False
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    return True


def managed_snapshot(root: Path) -> dict[Path, bytes]:
    """Read only managed files, pruning environments without traversing them."""
    paths = set()
    for relative in (".agents/skills", ".claude/skills"):
        directory = root / relative
        sync_skills.safe_path(root, directory)
        paths.update(directory / path for path in sync_skills.iter_skill_files(directory))
    for relative in (*SHARED_TOOLING, *SCAFFOLD_IF_MISSING, sync_skills.LOCK_RELATIVE_PATH):
        path = root / relative
        sync_skills.safe_path(root, path)
        if path.exists():
            if not path.is_file():
                raise UpdateError(f"expected a regular file: {path}")
            paths.add(path)
    return {path.relative_to(root): path.read_bytes() for path in sorted(paths)}


def update(repository_root: Path, source: str, ref: str, dry_run: bool) -> int:
    # Preflight the live tree before any staging/copying. Do not read local venvs.
    before = managed_snapshot(repository_root)
    lock = sync_skills.read_lock(repository_root)
    note_errors = sync_skills.inspect_notes(repository_root)
    if note_errors:
        raise UpdateError("; ".join(note_errors))
    local_skills = {
        skill.name: skill
        for skill in sync_skills.discover_skills(repository_root / ".agents/skills")
    }

    with tempfile.TemporaryDirectory(prefix="shared-skills-") as temporary:
        source_root, commit = resolve_source(source, ref, Path(temporary))
        sync_skills.safe_path(source_root, source_root / ".agents/skills")
        source_skills = [
            skill
            for skill in sync_skills.discover_skills(source_root / ".agents/skills")
            if skill.origin == "shared"
        ]
        conflicts = sorted(
            skill.name
            for skill in source_skills
            if skill.name in local_skills and local_skills[skill.name].origin == "local"
        )
        if conflicts:
            raise UpdateError(
                f"local skill(s) collide with shared skill names: {', '.join(conflicts)}. "
                "Rename the local skill before updating."
            )

        # The old parser must understand the source's metadata. Incompatible schema
        # upgrades fail closed; they require an explicit tooling migration first.
        stage = Path(temporary) / "stage"
        for relative in (".agents/skills", ".claude/skills"):
            (stage / relative).mkdir(parents=True)
        for relative, content in before.items():
            sync_skills.atomic_write_bytes(stage / relative, content)
        for skill in source_skills:
            copy_skill_directory(
                source_root / ".agents/skills" / skill.name,
                stage / ".agents/skills" / skill.name,
                False,
            )
        for relative in (*SHARED_TOOLING, *SCAFFOLD_IF_MISSING):
            sync_skills.safe_path(source_root, source_root / relative)
            if relative in SCAFFOLD_IF_MISSING and (stage / relative).exists():
                continue
            copy_file(source_root / relative, stage / relative, False)

        lock["shared_source"] = {"url": source, "ref": ref, "commit": commit}
        sync_skills.atomic_write(
            stage / sync_skills.LOCK_RELATIVE_PATH,
            json.dumps(lock, indent=2, sort_keys=True) + "\n",
        )
        # Execute the NEW tool in a clean interpreter, never the imported old module.
        # --dry-run validates in the disposable stage too, without changing the target.
        for arguments in ([], ["--check"]):
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(stage / "scripts/sync_skills.py"),
                    "--root",
                    str(stage),
                    *arguments,
                ],
                cwd=stage,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode:
                raise UpdateError(
                    f"staged sync failed; target unchanged:\n{result.stderr}{result.stdout}"
                )
        after = managed_snapshot(stage)
        # Publish provenance last, after content and generated adapters.
        ordered_paths = sorted(
            before.keys() | after.keys(),
            key=lambda path: (path == Path(sync_skills.LOCK_RELATIVE_PATH), path.as_posix()),
        )
        changes = {
            repository_root / path: after.get(path)
            for path in ordered_paths
            if before.get(path) != after.get(path)
        }
        # Fail if another writer changed managed content during staging.
        if managed_snapshot(repository_root) != before:
            raise UpdateError("target changed during staging; retry without concurrent writers")
        # Validate destination topology even for a dry run.
        for path in changes:
            sync_skills.safe_path(repository_root, path)
            if path.exists() and not path.is_file():
                raise UpdateError(f"file/directory conflict: {path}")
        if not dry_run:
            sync_skills.apply_changes(repository_root, changes)

    for path, content in changes.items():
        print(f"{'would ' if dry_run else ''}{'delete' if content is None else 'write'} {path}")
    shared_names = {skill.name for skill in source_skills}
    for name, skill in sorted(local_skills.items()):
        if skill.origin == "shared" and name not in shared_names:
            print(
                f"warning: shared skill {name!r} no longer exists in the source; "
                "delete it or change its metadata.origin to local",
                file=sys.stderr,
            )
    if dry_run:
        print(f"Dry run: {len(changes)} change(s) pending from {source} @ {ref}.")
    else:
        print(f"Shared skills updated from {source} @ {ref} ({len(changes)} change(s)).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        help="git URL or local directory of the template repository",
    )
    parser.add_argument(
        "--ref",
        default=DEFAULT_REF,
        help="tag or branch to fetch when --source is a git URL",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report the files that would change without writing",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=sync_skills.DEFAULT_REPOSITORY_ROOT,
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    try:
        return update(args.root.resolve(), args.source, args.ref, args.dry_run)
    except (UpdateError, sync_skills.LayoutError, OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
