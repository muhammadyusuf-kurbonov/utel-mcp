import os
import logging

IS_DEBUG_ENABLED = os.environ.get("MCP_DEBUG", "").lower() == "true"

UTEL_API_BASE_URL = os.environ.get("UTEL_API_BASE_URL", "")

if IS_DEBUG_ENABLED:
    logging.basicConfig(
        filename="/tmp/mcp_debug.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )
