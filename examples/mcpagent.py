# examples/mcp_agent.py

import asyncio
from mcpagentsdk import MCPAgencyClient, MCPAgentError

class MCPAgent:
    """
    MCPAgent is a high-level agent that uses MCPAgencyClient to interact with an MCP server.
    It demonstrates reading a resource and calling a tool via the MCP protocol.
    """

    def __init__(self, server_script: str):
        """
        :param server_script: Path to the Python file that runs the MCP server.
                              For example: "server.py"
        """
        self.client = MCPAgencyClient(
            transport="stdio",
            transport_params={
                "command": "python",
                "args": [server_script],
                "env": None  # Optionally pass custom env vars here
            }
        )

    async def start(self) -> None:
        """
        Connect to the MCP server.
        """
        await self.client.connect()

    async def stop(self) -> None:
        """
        Disconnect from the MCP server.
        """
        await self.client.disconnect()

    async def greet(self, name: str) -> str:
        """
        Reads the greeting resource for a given name.

        :param name: The name to greet.
        :return: A greeting message returned by the server.
        """
        resource_uri = f"greeting://{name}"
        return await self.client.read_resource(resource_uri)

    async def add_numbers(self, a: int, b: int) -> int:
        """
        Calls the 'add' tool on the server to add two numbers.

        :param a: First number
        :param b: Second number
        :return: Sum of a and b
        """
        result = await self.client.call_tool("add", arguments={"a": a, "b": b})
        return int(result)


# Example usage
async def main():
    # Path to your MCP server script
    server_script = "server.py"  # Replace with your server script path

    # Initialize the agent
    agent = MCPAgent(server_script)

    # Start the agent (connect to the server)
    await agent.start()

    try:
        # Read a resource
        greeting = await agent.greet("Alice")
        print("Greeting:", greeting)

        # Call a tool
        sum_result = await agent.add_numbers(10, 20)
        print("Sum:", sum_result)

    except MCPAgentError as e:
        print(f"An error occurred: {e}")

    finally:
        # Stop the agent (disconnect from the server)
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
