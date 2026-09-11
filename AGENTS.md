# Repository Agent Instructions

## Shared skills

- `.agents/skills` is the only source of truth for repository skills.
- When the task matches a skill description, read that skill's complete canonical
  `SKILL.md` before acting. Load only the referenced resources needed for the task.
- Create and edit skill instructions, scripts, references, and assets only under
  `.agents/skills/<skill-name>/`.
- Treat `.claude/skills`, `.agents/skills/CATALOG.md`, and `.agents/skills.lock` as
  generated output. Never edit them by hand.
- After any change under `.agents/skills`, run `scripts/sync_skills.py` with an
  available Python 3 launcher (`python3` on POSIX, `py -3` on Windows, or `python`
  when provided by the environment).
- Before finishing a skillset change, run the same command with `--check`.

## Skill authoring rules

- Write every skill in English: frontmatter, `SKILL.md`, scripts, references, and
  assets. Skill `description` values are validated to contain no Hangul.
- When a skill edits or analyses Korean text, keep the Korean terms, particles,
  endings, and example sentences that the instruction depends on, and explain them in
  English next to the Korean (한글 병기). Do not translate such examples into English.
- Frontmatter must contain `name`, `description`, and a `metadata` mapping with:
  - `group`: a logical grouping used by the generated catalog (`writing`, `visual`,
    `workflow`, `repo`, or a new lowercase-hyphen name).
  - `origin`: `shared` for skills maintained in the template repository and refreshed
    by `scripts/update_shared_skills.py`; `local` for skills that belong only to this
    repository. A `local` skill must not reuse a `shared` skill name.
- Only these extra top-level frontmatter keys are accepted and passed through to the
  Claude adapter: `license`, `compatibility`, `allowed-tools`, `argument-hint`,
  `disable-model-invocation`, `user-invocable`, `model`. Other harnesses ignore them.
- Put executable code and its environment files under `<skill-name>/scripts/`,
  documents under `references/`, and templates or static files under `assets/`.
  Local environments such as `.venv` are ignored by Git, by the content hash, and by
  the shared-skill updater.
- Do not edit `origin: shared` skills in a downstream repository. Propose the change
  in the template repository and pull it with `scripts/update_shared_skills.py`.

## Work notes

- Requirement interviews go to `_notes/grills/`, handoff briefs to
  `_notes/handoffs/to_codex|to_claude|to_human/`, named
  `<yymmdd-hhmm>-<topic-slug>.md`. `scripts/sync_skills.py --check` validates these
  filenames. Only the directory `README.md` files are committed.

## Python project

- Package code lives in `src/<package>/` and tests in `tests/`. The environment is
  managed by uv through `pyproject.toml`, `uv.lock`, and `.python-version`.
- Install with `uv sync`. Lint with `uv run ruff check .` and `uv run ruff format .`.
  Test with `uv run pytest`. Run every hook with `uv run pre-commit run --all-files`.
- Add runtime dependencies with `uv add <package>` and development tools with
  `uv add --group dev <package>`. Commit `uv.lock` together with `pyproject.toml`.
- `requires-python` is `>=3.10`. CI tests 3.10 and 3.12 on Ubuntu and Windows, so
  avoid platform-specific paths, shell assumptions, and newer syntax.
- `scripts/sync_skills.py`, `scripts/update_shared_skills.py`, and their tests must
  stay stdlib-only. They run with the system Python in `validate-skills.yml` and in
  repositories that do not use uv.
- Ruff excludes `.agents/`, `.claude/`, and `_notes/`. Do not reformat shared skills:
  their content hash is recorded in `.agents/skills.lock`.

## Repository work

- Preserve unrelated user changes.
- Keep changes focused and run checks relevant to the changed files.
- Add repository-wide build, test, and contribution conventions to this file as the
  project grows.
