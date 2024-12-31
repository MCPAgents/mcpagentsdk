# examples/server.py

from fastmcp.server import FastMCP

# Initialize the MCP server
server = FastMCP("Demo Server")

@server.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Provides a personalized greeting."""
    return f"Hello, {name}!"

@server.tool()
def add(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

if __name__ == "__main__":
    server.run()
