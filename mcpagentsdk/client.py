# mpcagency/client.py

import asyncio
from typing import Any, Dict, Optional
import sys

from mcpagentsdk.exceptions import (
    MCPAgentError,
    ConnectionError,
    ResourceError,
    ToolError,
)
from mcpagentsdk.transports.stdio_transport import StdioTransport
from mcpagentsdk.logger import logger
import json

class MCPAgencyClient:
    """
    MCPAgencyClient is a high-level abstraction for interacting with MCP servers.
    It uses standard I/O subprocesses to communicate with the server.
    """

    def __init__(
        self,
        transport: Optional[str] = "stdio",
        transport_params: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the MCPAgencyClient with the desired transport.

        :param transport: The transport mechanism to use ("stdio").
        :param transport_params: Parameters required for the chosen transport.
        """
        self.transport_type = transport
        self.transport_params = transport_params if transport_params else {}
        self.transport = None
        self.connected = False

        if self.transport_type == "stdio":
            self.transport = StdioTransport(
                command=self.transport_params.get("command", sys.executable),
                args=self.transport_params.get("args", []),
                env=self.transport_params.get("env", None),
            )
        else:
            logger.error(f"Unsupported transport type: {self.transport_type}")
            raise ValueError(f"Unsupported transport type: {self.transport_type}")

    async def connect(self) -> None:
        """
        Connect to the MCP server using the specified transport.
        """
        try:
            await self.transport.connect()
            self.connected = True
            logger.info("MCP session established successfully.")
        except ConnectionError as ce:
            logger.error(f"ConnectionError: {ce}")
            raise ce
        except Exception as e:
            logger.error(f"Failed to initialize MCP session: {e}")
            raise MCPAgentError(f"Failed to initialize MCP session: {e}") from e

    def connect_sync(self):
        """
        Synchronously connect to the MCP server using the specified transport.
        This method runs the asynchronous connect in an event loop.
        """
        asyncio.run(self.connect())

    async def disconnect(self) -> None:
        """
        Disconnect from the MCP server and close the transport.
        """
        try:
            if self.connected:
                await self.transport.disconnect()
                self.connected = False
                logger.info("MCP session closed.")
        except Exception as e:
            logger.error(f"Failed to disconnect: {e}")
            raise MCPAgentError(f"Failed to disconnect: {e}") from e

    def disconnect_sync(self):
        """
        Synchronously disconnect from the MCP server and close the transport.
        This method runs the asynchronous disconnect in an event loop.
        """
        asyncio.run(self.disconnect())

    async def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a JSON request to the MCP server and await a JSON response.

        :param request: The request dictionary to send.
        :return: The response dictionary from the server.
        """
        if not self.connected:
            logger.error("Client is not connected. Call connect() first.")
            raise ConnectionError("Client is not connected. Call connect() first.")

        try:
            # Serialize the request to JSON and send it
            request_json = json.dumps(request) + "\n"
            self.transport.writer.write(request_json)
            await self.transport.writer.drain()
            logger.info(f"Sent request: {request}")

            # Read the response line
            response_line = await self.transport.reader.readline()
            if not response_line:
                raise MCPAgentError("No response received from the server.")

            response = json.loads(response_line.strip())
            logger.info(f"Received response: {response}")
            return response
        except json.JSONDecodeError as jde:
            logger.error(f"JSON decode error: {jde}")
            raise MCPAgentError(f"JSON decode error: {jde}") from jde
        except Exception as e:
            logger.error(f"Failed to send request: {e}")
            raise MCPAgentError(f"Failed to send request: {e}") from e

    async def read_resource(self, resource_uri: str) -> Any:
        """
        Read a resource from the MCP server.

        :param resource_uri: The URI of the resource to read.
        :return: The content of the resource.
        """
        request = {
            "action": "read_resource",
            "uri": resource_uri
        }
        response = await self.send_request(request)
        if response.get("status") == "success":
            return response.get("data")
        else:
            error_msg = response.get("error", "Unknown error")
            logger.error(f"Failed to read resource '{resource_uri}': {error_msg}")
            raise ResourceError(f"Failed to read resource '{resource_uri}': {error_msg}")

    def read_resource_sync(self, resource_uri: str) -> Any:
        """
        Synchronously read a resource from the MCP server.
        This method runs the asynchronous read_resource in an event loop.

        :param resource_uri: The URI of the resource to read.
        :return: The content of the resource.
        """
        return asyncio.run(self.read_resource(resource_uri))

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool exposed by the MCP server.

        :param tool_name: The name of the tool to call.
        :param arguments: A dictionary of arguments to pass to the tool.
        :return: The result returned by the tool.
        """
        request = {
            "action": "call_tool",
            "tool": tool_name,
            "arguments": arguments
        }
        response = await self.send_request(request)
        if response.get("status") == "success":
            return response.get("data")
        else:
            error_msg = response.get("error", "Unknown error")
            logger.error(f"Failed to call tool '{tool_name}': {error_msg}")
            raise ToolError(f"Failed to call tool '{tool_name}': {error_msg}")

    def call_tool_sync(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Synchronously call a tool exposed by the MCP server.
        This method runs the asynchronous call_tool in an event loop.

        :param tool_name: The name of the tool to call.
        :param arguments: A dictionary of arguments to pass to the tool.
        :return: The result returned by the tool.
        """
        return asyncio.run(self.call_tool(tool_name, arguments))
