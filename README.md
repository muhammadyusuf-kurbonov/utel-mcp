# utel-mcp

An [MCP](https://modelcontextprotocol.io/) server that wraps the UTEL IP-telephony REST API as MCP tools and documentation **resources**.  
Lets LLM agents discover and call UTEL API endpoints with proper auth baked in.

Built with [FastMCP](https://github.com/jlowin/fastmcp) (Python).

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) — package manager

## Setup

```sh
uv sync
```

## Configuration

The server is configured through environment variables (no `.env` file is loaded automatically):

| Variable | Required | Description |
|---|---|---|
| `UTEL_API_BASE_URL` | Yes | Base URL of the UTEL API instance (e.g. `https://api.cc999.utel.uz/api/v1`) |
| `HTTP_BEARER_TOKEN` | No | Sets an `Authorization: Bearer <token>` header on every request |
| `MCP_DEBUG` | No | Set to `"true"` to log full request payloads to `/tmp/mcp_debug.log` |

## Usage

```sh
uv run utel-mcp
```

This starts the MCP server on **stdio transport** — it communicates over standard input/output.  
Configure your MCP host (Claude Desktop, OpenCode, etc.) to launch it as a stdio subprocess.

## Tools

### `send_request`

Sends an authenticated HTTP request to the UTEL API. The `path` is joined with `UTEL_API_BASE_URL`.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | — | API path, e.g. `/ats/ps-user`. Leading slash recommended. |
| `method` | string | `"GET"` | HTTP method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`) |
| `headers` | object | `null` | Extra headers (merged on top of defaults) |
| `json_data` | object | `null` | JSON body |
| `params` | object | `null` | Query parameters |

**Returns:** Status code + response body as a string.

Pre-configured headers on every request: `Accept: application/json`, `Content-Type: application/json`, and `Authorization: Bearer <token>` (if `HTTP_BEARER_TOKEN` is set).

## Resources (Built-in API Documentation)

The server exposes the full UTEL API reference as MCP resources, so agents can look up endpoint details without leaving the conversation:

| Resource | Description |
|---|---|
| `utel://api` | Index of all available documentation topics |
| `utel://api/{topic}` | Documentation for a specific topic |
| `utel://api/reference` | Full comprehensive API reference (all topics) |
| `utel://skill` | Same as `reference` — alias for agent skill context |

Available topics: `intro`, `auth`, `call-history`, `statistics`, `trunks`, `voice-messages`, `sip-users`, `ivr`, `groups`, `queues`, `time-rules`, `voicemail`, `smart-redirect`, `webhooks`, `extension-ranges`.

## Source Layout

```
src/utel_mcp/
├── __init__.py    ← MCP server instance, tool/resource registration, entry point
├── config.py      ← Environment variable loading
├── utils.py       ← Shared helpers (header construction)
├── handlers.py    ← Tool and resource implementations
└── docs.py        ← Inline API documentation data
```

## License

MIT
