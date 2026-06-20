# utel-mcp

An [MCP](https://modelcontextprotocol.io/) server that wraps the UTEL IP-telephony REST API as MCP tools.  
Lets LLM agents make authenticated HTTP requests to the UTEL API via a simple MCP tool interface.

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
| `HTTP_BEARER_TOKEN` | No | Sets an `Authorization: Bearer <token>` header on every request |
| `HTTP_DEFAULT_HEADERS` | No | JSON string of extra headers (e.g. `{"X-Custom": "value"}`). Invalid JSON is silently ignored. |
| `MCP_DEBUG` | No | Set to `"true"` to log full request payloads to `/tmp/mcp_debug.log` |

## Usage

```sh
uv run utel-mcp
```

This starts the MCP server on **stdio transport** — it communicates over standard input/output.  
Configure your MCP host (Claude Desktop, OpenCode, etc.) to launch it as a stdio subprocess.

## Tools

### `send_request`

Sends an HTTP request with the configured auth headers baked in.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | — | Target URL |
| `method` | string | `"GET"` | HTTP method |
| `headers` | object | `null` | Extra headers (merged on top of configured defaults) |
| `json_data` | object | `null` | JSON body |
| `params` | object | `null` | Query parameters |

**Returns:** Status code + response body as a string.

## License

MIT
