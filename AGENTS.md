# utel-mcp — Agent Instructions

## What this is

An MCP server that wraps the UTEL IP-telephony REST API as MCP tools.  
All code lives in a single module: `src/utel_mcp/__init__.py`.

## Commands

```sh
# run the server (stdio transport)
uv run utel-mcp

# add / remove dependencies
uv add <package>
uv remove <package>

# install everything
uv sync
```

There is no conventional `python -m` entry point — the `utel-mcp` console script is the only way to run it.

## Architecture notes

- **Single file.** `src/utel_mcp/__init__.py` contains everything: config loading, the MCP server instance, the single `send_request` tool, and the `main()` entry point.
- **Stdio transport.** The MCP server communicates over stdin/stdout (`mcp.run(transport="stdio")`). No TCP/SSE server to start.
- **No tests, no CI, no linter config.** The project is at its very beginning. Any of these may need to be set up from scratch.

## Configuration

Everything is driven by environment variables (no `.env` file is loaded automatically):

| Variable | Purpose |
|---|---|
| `HTTP_BEARER_TOKEN` | Sets an `Authorization: Bearer <token>` header on every request |
| `MCP_DEBUG` | Set to `"true"` to log full request payloads to `/tmp/mcp_debug.log` |

## Project conventions

- **Python 3.11+** (requires `>=3.11`; dev machine runs 3.14).
- **`uv`** is the package manager. Do not use `pip` directly.
- **`uv_build`** build backend (not `setuptools`).
- **No `.gitignore` yet.** The `__pycache__/` directory and `.venv/` should be excluded when one is created. The stale `__pycache__/main.cpython-*.pyc` is an orphan from a past `main.py`.
- **No commits yet** — the repo is a fresh `git init` with zero commits.

## Source layout

```
src/utel_mcp/__init__.py   ← the entire application
```

`__pycache__/main.cpython-*.pyc` is a stale artifact — no `main.py` file currently exists on disk.
