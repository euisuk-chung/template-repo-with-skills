# Canonical skills

This directory is the single source of truth for shared repository skills. See
`CATALOG.md` (generated) for the grouped index.

Create each skill at `<skill-name>/SKILL.md`, then run:

```shell
# POSIX
python3 scripts/sync_skills.py

# Windows
py -3 scripts/sync_skills.py
```

Write every skill in English. Keep Korean terms and examples only where a skill
handles Korean text, and explain them in English alongside.

Frontmatter requires `name`, `description`, and `metadata` with `group` and `origin`
(`shared` or `local`). Keep `name` as a one-line YAML scalar. `description` may be a
one-line value or a YAML block scalar and must be English. The directory name must
match `name` and use lowercase letters, digits, and hyphens.

The stdlib-only validator supports a restricted YAML subset: flat, two-space-indented
metadata string entries (with comments), one-line strings, and description blocks.
Use single quotes or JSON-compatible double quotes for ambiguous strings, especially
colon-space, numeric/date-like values and YAML booleans. Lists, aliases, nested maps,
and scalar continuations are rejected. `allowed-tools` is a one-line string.
Only `disable-model-invocation` and `user-invocable` accept unquoted `true`/`false`.

Optional `scripts/`, `references/`, `assets/`, and `agents/` directories belong inside
the canonical skill directory. Reference their files relative to the canonical
`SKILL.md`. Keep executable code and environment files in `scripts/`.

Static PNG assets are included in Git, updates and content hashes. Put disposable
previews under `_generated/`, which is pruned alongside local environments and caches.
Non-ignored symlinks/reparse points are rejected, including directory links.
Known UTF-8 text formats have CRLF/CR normalised to LF for hashing only; binary and
unknown formats remain byte-exact. See the root README for the complete format list.

Refresh `origin: shared` skills from the template repository with:

```shell
python3 scripts/update_shared_skills.py --ref <tag-or-branch>
```
