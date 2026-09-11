# Renderer setup

The optional renderer converts `.excalidraw` JSON into a PNG so an agent can inspect
the visual result. It requires Python 3.11 or newer, `uv`, Playwright, and Chromium.
`uv` downloads a compatible interpreter when the system Python is older.

The renderer and its locked environment live in the canonical skill's `scripts/`
directory. From the repository root:

```shell
cd .agents/skills/excalidraw-diagram/scripts
uv sync
uv run playwright install chromium
```

Render a diagram:

```shell
uv run python render_excalidraw.py <path-to-file.excalidraw>
```

The PNG is written next to the input unless `--output` is supplied. Use `--scale` and
`--width` to control screenshot density and maximum viewport width.

## Keeping the environment out of the skill tree

By default `uv sync` creates `scripts/.venv`. That directory is ignored by Git and by
the skill content hash, and `scripts/update_shared_skills.py` leaves it alone. To keep
the environment outside the repository entirely, point `uv` at another location before
running the commands above:

```shell
export UV_PROJECT_ENVIRONMENT="$HOME/.cache/agent-skills/excalidraw-diagram"
```

## When rendering is unavailable

The renderer loads Excalidraw's browser module from `esm.sh`, so the first render also
requires network access to that host. If setup, the Python version, or network access
is unavailable, validate the JSON and report that the PNG preview was not visually
inspected.
