---
name: handoff
description: Write a self-contained task or review brief for a new Codex session, Claude session, or human recipient to act on without chat history. Use when the user explicitly requests a handoff, session transfer, or instructions for another worker.
argument-hint: "recipient (codex, claude, human), task or review request, and focus"
disable-model-invocation: true
metadata:
  group: workflow
  origin: shared
---

# Standalone task and review handoff

Create an actionable brief under `_notes/handoffs/<recipient>/`. The recipient must
be able to start the requested work using this document and the identified repository
or supplied artifacts, without access to the author's conversation or memory.

Lead with the assignment: what to do, why, on which inputs, and what result to return.
Include current state and history only when they affect execution.

## Identify recipient and assignment

- `to_codex/`: instructions for a new Codex session.
- `to_claude/`: instructions for a new Claude session.
- `to_human/`: instructions for a person, such as a developer or reviewer.

These folders identify the recipient, not the author. A document written by Codex for
Claude belongs in `to_claude/`. Use the recipient specified by the user or clearly
established in context. If ambiguous, ask a short clarification with the host's
available question mechanism; do not silently choose the current host. Create multiple
recipient versions only when requested, and make each independently actionable.

Determine the requested work type: implementation, review, investigation, or another
explicit assignment. Preserve that scope. A review request does not authorize fixes,
and a handoff must not expand permission to commit, push, deploy, or contact others.

## Make the brief self-contained

Include the objective, essential background, confirmed decisions, constraints, inputs,
work sequence, expected deliverables, acceptance criteria, and unresolved dependencies.
Never rely on phrases such as “as discussed,” “continue the above,” or “use my memory.”

For implementation, specify intended behavior, affected interfaces, non-goals, and
observable tests. For review, identify the review target and baseline (commit range,
working-tree changes, or named artifacts), review questions, priorities, and report
format. Request file/symbol locations and evidence for findings; distinguish defects
from suggestions. For a human recipient, explain commands, working directories,
expected results, and required access without relying on agent-specific tools.

Name repository/artifact locations and relevant environment prerequisites. Repository
paths in the brief are relative to the repository root unless explicitly stated.
Identify uncommitted or untracked inputs and whether the recipient has access to them;
do not imply that a branch or commit includes working-tree changes. If essential
inputs cannot be accessed, state that prerequisite before the first execution step.

Tell the recipient to compare the documented baseline with the actual checkout before
acting, preserve unrelated changes, and reassess affected instructions if the state
has changed. Do not require a particular client version, model, or tool unless the
assignment actually depends on it.

## Gather current evidence

Read the repository instructions and the files relevant to the task. When the workspace
uses Git, inspect at least:

```shell
git status --short --branch
git diff --stat
git diff --cached --stat
git log --oneline -8
```

Inspect the substantive diff and relevant file contents when a summary alone cannot
show what is complete. Determine the current branch and commit from command output; do
not assume a branch name, remote, upstream, or deployment workflow. Check those only
when they matter to the next action.

If the workspace does not use Git, record that and derive state from the available
files and task evidence.

## Keep evidence classes separate

- **Verified:** observed in source, command output, tests, a real request, or a visual
  check. Record the exact command or artifact and meaningful result.
- **Inferred:** concluded from reading or partial evidence. State why it is plausible.
- **Unverified:** expected but not checked. State the exact next check.
- **Blocked:** cannot proceed without a decision, permission, dependency, credential,
  or external state change. Name the missing item and owner.

Local success does not prove CI, staging, or production behavior. Record each
environment separately.

## Include essentials and link supporting detail

Summarize every decision or constraint needed to understand the assignment inside the
brief, even when it already exists elsewhere. Link to repository documents and supplied
artifacts for implementation details and evidence, and explain when to read each one.
Links supplement the assignment; they do not replace it or require access to old chats.

## Protect sensitive data

Do not read secret files solely for the handoff. Never copy credentials, tokens,
cookies, private keys, personal data, or confidential source content into the document.
Refer to secret variable names or credential locations only when needed and replace any
observed value with `<redacted>`.

## Write or update the handoff

Use `_notes/handoffs/<recipient>/<yymmdd-hhmm>-<topic-slug>.md`. Before creating a file, read the repository's
`_notes/README.md` naming rules and inspect existing notes. Use a stable descriptive
English slug with lowercase letters, digits, and single hyphens. Match the slug of
an existing grill record for the same topic, excluding its timestamp. Use the actual
creation time for the filename prefix (two-digit year, month, day, then 24-hour hour
and minute). Use the project timezone, or the current environment's timezone if none
is specified; record its name and UTC offset in the document. Do not append author or
harness names, or duplicate suffixes such as `-2`, `-final`, or `-latest`. For a different
topic or separate assignment with the same proposed name, add a meaningful qualifier
such as `search-filter-review`. If a handoff for the same recipient and assignment
exists, find it by topic and content regardless of timestamp, read it first, and
update it rather than creating duplicates. Keep its filename and Created value;
update Updated with the actual current time. Do not overwrite
an implementation brief with a separate review request or another recipient's brief.
Preserve still-relevant failed attempts and the reasons they failed.

```markdown
# <Task> — Handoff

> Recipient: codex / claude / human
> Request type: implementation / review / investigation / other
> Created: yymmdd-hhmm
> Updated: yymmdd-hhmm
> Timezone: <timezone name and UTC offset>
> Baseline: branch `<branch-or-n/a>` · commit `<sha-or-n/a>`

## Assignment

What the recipient must do and return, stated as a direct instruction.

## Context and intended outcome

Why this work is needed, essential terminology, confirmed decisions, and intended
behavior. Include enough detail to understand the task without any previous chat.

## Scope and constraints

In-scope and out-of-scope work, compatibility requirements, and action boundaries.
For reviews, explicitly state whether edits are requested or findings only.

## Inputs and starting point

Repository/artifact location, checkout or review baseline, relevant files/symbols,
environment prerequisites, working directories, and access to uncommitted inputs.

## Current state

What works, what is incomplete, and whether each change is committed, staged, or only
present in the working tree.

| Path | State | Notes |
| --- | --- | --- |
| `path/to/file` | modified / new / unchanged | concrete status |

## Verified evidence

Commands or checks run and their meaningful results. Include failures.

## Inferences, unknowns, and blockers

Separate each item and state what would resolve it.

## Execution steps

Start by confirming the inputs and baseline. Then give ordered, concrete steps with
file/symbol locations. For reviews, specify review questions and the exact diff or
artifacts to inspect. State what to do if a required input or decision is missing.

## Verification to run

Repository-specific commands and manual checks. Do not invent commands that were not
confirmed from repository configuration or instructions.

## Deliverables and completion criteria

Expected files or report, output location/format, and observable conditions for
completion. For a review, require findings with severity, location, evidence, impact,
and remaining verification gaps; explicitly report when no findings are supported.

## Relevant skills and references

Only skills and repository paths that actually exist and apply to the next work.
```

Before finishing, read the brief as a recipient with no chat history. Confirm that
the assignment, first action, inputs, boundaries, deliverable, and completion criteria
can all be found in the document. Mark missing evidence rather than inventing it.
Return a link to the brief and a short invocation the user can paste into a new
session, or a short request message for the human recipient. Do not send it externally.

## Boundaries

- Do not change implementation, commit, push, deploy, or contact external systems as
  part of creating the handoff.
- Do not claim a check passed unless it ran successfully in the stated environment.
- Do not list the conversation chronologically.
- Do not erase a useful failure record merely because a later approach worked.
- Keep the document concise enough that the next session can act before rereading the
  whole repository.
