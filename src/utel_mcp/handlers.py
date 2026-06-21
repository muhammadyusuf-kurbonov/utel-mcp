import json
import logging
import posixpath
from typing import Any, Dict, Literal, Optional

import httpx
from mcp.server.fastmcp import FastMCP

from utel_mcp import mcp, docs
from utel_mcp.config import IS_DEBUG_ENABLED, UTEL_API_BASE_URL
from utel_mcp.utils import load_predefined_headers


@mcp.tool()
async def send_request(
    path: str,
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"] = "GET",
    headers: Optional[Dict[str, str]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> str:
    """Send a request to the UTEL API. The `path` is joined with `UTEL_API_BASE_URL` (env var). Use a leading slash, e.g. `/ats/ps-user`. The `Authorization: Bearer` token (`HTTP_BEARER_TOKEN`) is already included on every request."""
    if not UTEL_API_BASE_URL:
        return "Error: `UTEL_API_BASE_URL` env var is not set."

    resolved_path = posixpath.normpath("/" + path.lstrip("/"))
    url = UTEL_API_BASE_URL.rstrip("/") + resolved_path

    merged_headers = load_predefined_headers()
    if headers:
        merged_headers.update(headers)

    if IS_DEBUG_ENABLED:
        debug_payload = {
            "URL": url,
            "Method": method,
            "Final_Headers": merged_headers,
            "Query_Params": params,
            "JSON_Body": json_data,
        }
        logging.info(f"FINAL REQUEST PARAMS:\n{json.dumps(debug_payload, indent=2)}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=merged_headers,
                json=json_data,
                params=params,
                follow_redirects=True,
            )
            return f"Status Code: {response.status_code}\n\n{response.text}"
        except httpx.RequestError as exc:
            return f"An error occurred: {exc}"


@mcp.resource("utel://api")
async def get_api_index() -> str:
    """Index of all UTEL API documentation topics."""
    lines = ["# UTEL API Documentation", "", "Available topics:"]
    topics = [
        ("intro", "Base URL, headers, common errors"),
        ("auth", "Login, Me, Change password, Logout"),
        ("call-history", "Call history list with filters"),
        ("statistics", "Calls count, by hour/day/month/external/users"),
        ("trunks", "SIP trunk CRUD and reregister"),
        ("voice-messages", "Voicemail message list, unread count, mark as read"),
        ("sip-users", "SIP user CRUD, redirects, contacts"),
        ("ivr", "IVR CRUD and audio upload"),
        ("groups", "Ring group CRUD"),
        ("queues", "Queue CRUD, types, hold music"),
        ("time-rules", "Time rule CRUD"),
        ("voicemail", "Voicemail CRUD"),
        ("smart-redirect", "Smart redirect CRUD"),
        ("webhooks", "Webhook list and replace"),
        ("extension-ranges", "Extension number ranges by module"),
        ("reference", "Full comprehensive API reference (all topics)"),
    ]
    for slug, desc in topics:
        lines.append(f"- `utel://api/{slug}` — {desc}")
    lines.append("")
    lines.append("### Skill")
    lines.append("- `utel://skill` — Full UTEL API skill document (same as reference)")
    return "\n".join(lines)


@mcp.resource("utel://api/reference")
async def get_api_reference() -> str:
    """Full comprehensive UTEL API reference — all endpoints, fields, types, and usage patterns."""
    return docs.UTEL_API_REFERENCE


@mcp.resource("utel://skill")
async def get_skill() -> str:
    """Full UTEL API skill document — comprehensive API reference for agents. Use this as context when working with UTEL API."""
    return docs.UTEL_API_REFERENCE


@mcp.resource("utel://api/{topic}")
async def get_api_doc(topic: str) -> str:
    """Documentation for a specific UTEL API topic."""
    doc = docs.UTEL_API_DOCS.get(topic)
    if doc is not None:
        return doc
    available = ", ".join(sorted(docs.UTEL_API_DOCS.keys()))
    return f"Unknown topic '{topic}'. Available topics: {available}"
