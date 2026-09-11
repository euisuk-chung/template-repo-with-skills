---
name: excalidraw-diagram
description: Create or edit Excalidraw JSON diagrams for workflows, architectures, comparisons, and concepts. Use when the requested deliverable is an editable .excalidraw file or an Excalidraw-based technical visual.
metadata:
  group: visual
  origin: shared
---

# Excalidraw diagram

Create an editable `.excalidraw` JSON file that communicates relationships, sequence,
or structure visually. Produce a PNG preview when the bundled renderer is available.

## Load only what the task needs

- Always read `references/color-palette.md` before choosing colors.
- Read `references/element-templates.md` before authoring raw Excalidraw elements.
- Read `references/json-schema.md` when validating unfamiliar fields or bindings.
- Read `references/setup.md` only when the renderer is not installed or the user asks
  to configure it. The renderer code and its locked environment live in `scripts/`.

Resolve these paths from the canonical `.agents/skills/excalidraw-diagram/` directory,
not from a generated harness adapter.

## Plan the visual

Determine the audience and required depth first:

- Use a simple conceptual diagram for a mental model or quick overview.
- Use a detailed technical diagram when the visual must teach a real system. Inspect
  the repository or authoritative sources for actual interfaces, event names, payloads,
  and constraints before drawing them.

Identify the main claim or learning outcome. Map concepts to structures that reflect
their behavior:

| Relationship | Useful visual structure |
| --- | --- |
| sequence or lifecycle | timeline or directed flow |
| one source to many outputs | fan-out |
| many inputs to one result | convergence or funnel |
| hierarchy or containment | tree or nested regions |
| repeated improvement | cycle |
| transformation | before → process → after |
| alternatives or tradeoffs | side-by-side comparison |

Use one clear reading direction. For a detailed visual, provide three useful zoom
levels where appropriate: a summary flow, labeled sections, and concrete evidence
inside sections.

## Design rules

- Let geometry carry meaning. Avoid a uniform grid of labeled cards.
- Default to free-floating text; add a container only for grouping, connection, or a
  semantic shape such as a decision diamond.
- Show every important relationship with a line or arrow.
- Use size, whitespace, and text hierarchy to emphasize the main idea.
- Use colors only from `references/color-palette.md` and assign them consistently by
  meaning.
- Use `opacity: 100`. Default to `roughness: 0` for technical diagrams unless the user
  asks for a hand-drawn style.
- Keep readable text in `text` and `originalText`. Do not place JSON syntax or styling
  metadata in visible labels.
- Prefer `fontFamily: 3`; keep ordinary labels readable at the exported size.
- Use stable descriptive element IDs and ensure bindings reference existing IDs.

For large diagrams, create and validate one coherent section at a time, then review
cross-section connections as a whole. For a small diagram, a single direct edit is
fine. Use a generator only when repeated deterministic layouts make it easier to
maintain than direct JSON.

## Create the file

Use the standard wrapper:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

Place the output where the user requested. If no location was provided, choose a
descriptive filename in the current working directory and state that choice.

## Render and inspect

JSON validation alone cannot catch clipping, overlaps, unclear routing, or imbalance.
After each meaningful draft:

1. Run the bundled renderer from the canonical skill's `scripts` directory:

   ```shell
   cd .agents/skills/excalidraw-diagram/scripts
   uv run python render_excalidraw.py <path-to-file.excalidraw>
   ```

2. View the generated PNG with the host's image-viewing capability.
3. Check the conceptual flow before checking visual defects.
4. Fix clipped text, overlaps, ambiguous labels, crossed arrows, uneven spacing,
   unreadable type, and unbalanced composition.
5. Render and inspect again until the diagram is ready to share.

If rendering cannot run because dependencies, browser binaries, or network access are
unavailable, still validate the JSON structure and bindings. Tell the user that visual
inspection remains unverified and provide the setup command from `references/setup.md`.

## Final check

- The diagram teaches or demonstrates something that prose alone would not show as
  clearly.
- Concrete technical details are accurate and sourced from the inspected system.
- The main path is obvious without reading every label.
- Text fits, elements do not overlap, and arrows land on their intended targets.
- The `.excalidraw` file remains editable and the preview reflects the final JSON.
