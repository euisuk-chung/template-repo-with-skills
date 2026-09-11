---
name: grill-me
description: Turn an ambiguous requirement or design idea into implementation-ready decisions through a focused interview and save a decision record. Use only when the user explicitly asks to be interviewed, grilled, or guided through unresolved choices.
argument-hint: "requirement or design topic to clarify"
disable-model-invocation: true
metadata:
  group: workflow
  origin: shared
---

# Requirements and design interview

Clarify an ambiguous request without implementing it. The outcome is a reviewable set
of requirements and design decisions saved under `_notes/grills/`.

## Separate facts from choices

Inspect the repository before asking questions. Read applicable agent instructions,
project documentation, configuration, tests, and relevant code. Use the repository's
available search and read tools to answer questions about the current implementation.

Ask the user only about information that cannot be discovered from the repository:
intent, priorities, acceptable tradeoffs, product behavior, operational constraints,
and ownership decisions. Do not ask the user to locate files, restate code behavior, or
provide facts that can be checked safely.

When no repository or source material is available, identify assumptions explicitly
and ask only for the facts required to choose between materially different outcomes.

## Interview in rounds

Treat unresolved decisions as a dependency tree. In each round, ask the independent
questions that are currently answerable. Keep each batch within the active question
tool's limits; one question is sufficient when later choices depend on its answer.
Wait for the answers before opening dependent questions.

### Use the host's question tool

- In Claude Code, use `AskUserQuestion` for clarification, unresolved choices, and
  confirmation of the final decision summary. Do not substitute a Markdown
  questionnaire when this tool is available and permitted.
- In other harnesses, use the available structured user-input tool for the same
  purpose, following its current schema and execution-mode restrictions. Do not
  assume that a Claude tool name exists in another host.
- If no suitable question tool is available or permitted in the current mode, ask
  concise questions in the conversation and wait for the user's reply. This is a
  fallback, not the default interview format.
- With an asynchronous question tool, continue only independent investigation while
  an answer is pending. Do not treat silence, a timeout, a preselected option, or a
  skipped question as agreement. Keep unanswered items open or explicitly deferred.

For each tool question, include a short decision title, a self-contained question,
and enough context to explain why the choice matters. For finite choices, provide
distinct options with concise tradeoffs and mark the recommended option. Allow the
user to provide a different answer through the tool's supported free-text mechanism.
For genuinely open-ended questions, use free text if the tool supports it.

Only when using the conversation fallback, format questions as:

```text
Q1 — <decision title>
<question and one sentence explaining why the choice matters>
Recommended: <default choice and concise rationale>
```

Offer mutually exclusive options when the decision has a finite set. Include the
recommended option first. Do not reopen choices the user has already made unless new
repository evidence creates a direct conflict; if so, show that evidence.

## Decision axes

Use only the axes relevant to the topic:

- problem, target user, and measurable outcome;
- in-scope behavior and explicit non-goals;
- main flow, edge cases, and failure recovery;
- data inputs, outputs, ownership, retention, and migration;
- interfaces, dependencies, and compatibility boundaries;
- security, privacy, permissions, and abuse cases;
- performance, reliability, observability, and operational ownership;
- rollout, reversibility, and backward compatibility;
- acceptance criteria and verification evidence.

Derive repository-specific axes from existing architecture and policy documents. Do
not embed assumptions from another project.

## Workflow

1. Restate the topic and the current understanding in one short paragraph.
2. Record facts already established by repository evidence.
3. Run question rounds through the host's question tool (or the fallback above) until
   the remaining uncertainty no longer blocks a design.
4. Summarize the decisions, assumptions, non-goals, and open questions.
5. Use the same question mechanism to ask the user to confirm or correct that summary.
6. After the user confirms the summary or supplies corrections, write or update the
   decision record. Distinguish confirmed choices from any remaining open questions.
   Do not modify product code.

## Decision record

Use `_notes/grills/<yymmdd-hhmm>-<topic-slug>.md`. Before creating a file, read the repository's
`_notes/README.md` naming rules and inspect existing notes. Use a stable descriptive
English slug with lowercase letters, digits, and single hyphens. Match the slug of
an existing handoff for the same topic, excluding its timestamp. Use the actual creation
time for the filename prefix (two-digit year, month, day, then 24-hour hour and minute).
Use the project timezone, or the current environment's timezone if none is specified;
record its name and UTC offset in the document. Do not append author or harness names,
or duplicate suffixes such as `-2`, `-final`, or `-latest`. For a different topic with
the same proposed name, add a meaningful scope qualifier instead.
Find existing records by topic and content, not just timestamp. If a record already
exists for this request, read it first, retain its filename and Created value, update
Updated with the actual current time, update decisions in place, and
preserve superseded decisions with a short reason when that history remains useful.

```markdown
# <Topic> — Decision record

> Goal: <one sentence>
> Created: yymmdd-hhmm
> Updated: yymmdd-hhmm
> Timezone: <timezone name and UTC offset>

## Context

Repository facts and the problem being solved. Link to existing documents rather than
copying them.

## Decisions

| ID | Decision | Choice | Rationale | Source |
| --- | --- | --- | --- | --- |
| D1 | ... | ... | ... | user / repository evidence |

## Constraints and assumptions

Confirmed constraints and assumptions that still require verification.

## Out of scope

What will not be implemented and why.

## Expected impact

Likely files, interfaces, data, operations, and users affected. Mark this as an
estimate until implementation confirms it.

## Open questions

Unresolved items, owner, and the evidence needed to close each one.

## Acceptance criteria

Observable behavior and the repository-specific checks that should prove it.
```

## Boundaries

- Do not implement code as part of this skill.
- Do not invent repository conventions or verification commands.
- Do not force every decision axis into the document; omit irrelevant sections.
- Do not continue interviewing after the remaining questions can safely be deferred to
  implementation.
