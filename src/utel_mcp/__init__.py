from mcp.server.fastmcp import FastMCP

from . import config

mcp = FastMCP("MCP server to use as RestAPI client for Utel API")

from . import docs
from . import utils
from . import handlers


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
