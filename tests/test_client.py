import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from mcpagentsdk import MCPAgencyClient, ResourceError, ToolError


class TestMCPAgencyClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Initialize MCPAgencyClient with mocked transport
        self.client = MCPAgencyClient(
            transport="stdio",
            transport_params={
                "command": "python",
                "args": ["dummy_server.py"],
                "env": None
            }
        )
        # Mock the transport's connect method
        self.client.transport.connect = AsyncMock()
        # Mock the session
        self.client.session = AsyncMock()
        self.client.session.read_resource = AsyncMock(return_value="Hello, Test!")
        self.client.session.call_tool = AsyncMock(return_value=42)

    async def test_connect_disconnect(self):
        await self.client.connect()
        self.client.transport.connect.assert_awaited_once()
        self.client.session.initialize.assert_awaited_once()

        await self.client.disconnect()
        self.client.session.close.assert_awaited_once()
        self.client.transport.disconnect.assert_awaited_once()

    async def test_read_resource_success(self):
        resource = await self.client.read_resource("greeting://Test")
        self.client.session.read_resource.assert_awaited_once_with("greeting://Test")
        self.assertEqual(resource, "Hello, Test!")

    async def test_read_resource_failure(self):
        self.client.session.read_resource.side_effect = Exception("Read failed")
        with self.assertRaises(ResourceError):
            await self.client.read_resource("greeting://Test")

    async def test_call_tool_success(self):
        result = await self.client.call_tool("add", {"a": 1, "b": 2})
        self.client.session.call_tool.assert_awaited_once_with("add", arguments={"a": 1, "b": 2})
        self.assertEqual(result, 42)

    async def test_call_tool_failure(self):
        self.client.session.call_tool.side_effect = Exception("Tool failed")
        with self.assertRaises(ToolError):
            await self.client.call_tool("add", {"a": 1, "b": 2})

    def test_connect_sync(self):
        with patch('asyncio.run') as mock_run:
            self.client.connect_sync()
            mock_run.assert_called_once_with(self.client.connect())

    def test_disconnect_sync(self):
        with patch('asyncio.run') as mock_run:
            self.client.disconnect_sync()
            mock_run.assert_called_once_with(self.client.disconnect())

    def test_read_resource_sync(self):
        with patch('asyncio.run', return_value="Hello, Sync Test!") as mock_run:
            result = self.client.read_resource_sync("greeting://SyncTest")
            mock_run.assert_called_once_with(self.client.read_resource("greeting://SyncTest"))
            self.assertEqual(result, "Hello, Sync Test!")

    def test_call_tool_sync(self):
        with patch('asyncio.run', return_value=99) as mock_run:
            result = self.client.call_tool_sync("multiply", {"a": 9, "b": 11})
            mock_run.assert_called_once_with(self.client.call_tool("multiply", {"a": 9, "b": 11}))
            self.assertEqual(result, 99)


if __name__ == "__main__":
    unittest.main()
