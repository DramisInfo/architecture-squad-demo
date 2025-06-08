"""
Base test class for Diagram Generator MCP server tests.

This module provides common functionality and setup for all test classes.
"""

import sys
import json
from pathlib import Path
from typing import Any, Dict

import pytest
from mcp.types import TextContent
from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
from mcp.server.fastmcp import FastMCP

# Add the parent directory to the path so we can import the server modules
sys.path.insert(0, str(Path(__file__).parent.parent))


class BaseMCPTest:
    """Base class for all MCP server tests."""

    def create_test_server(self) -> FastMCP:
        """Create the diagram generator MCP server for testing."""
        from server import mcp
        return mcp

    async def call_tool_and_verify_success(self, client, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool and verify it returns a successful response.

        Args:
            client: MCP client session
            tool_name: Name of the tool to call
            params: Parameters to pass to the tool

        Returns:
            Parsed response data as dictionary

        Raises:
            AssertionError: If the tool call fails or returns invalid data
        """
        result = await client.call_tool(tool_name, params)

        # Verify successful execution
        assert not result.isError, f"Tool {tool_name} returned an error"
        assert len(
            result.content) == 1, f"Tool {tool_name} returned unexpected content length"
        assert isinstance(
            result.content[0], TextContent), f"Tool {tool_name} returned non-text content"

        # Parse the response
        response_data = json.loads(result.content[0].text)
        assert "success" in response_data, f"Tool {tool_name} response missing 'success' field"

        return response_data

    async def verify_diagram_response(self, response_data: Dict[str, Any], expected_format: str = "png"):
        """
        Verify that a diagram generation response has the expected structure.

        Args:
            response_data: Response data from diagram generation tool
            expected_format: Expected file format (default: png)
        """
        assert response_data["success"] is True, "Diagram generation failed"
        assert "file_path" in response_data, "Response missing file_path"
        assert "filename" in response_data, "Response missing filename"
        assert "format" in response_data, "Response missing format"
        assert response_data[
            "format"] == expected_format, f"Expected format {expected_format}, got {response_data['format']}"

        # Verify file path and filename are valid
        file_path = response_data["file_path"]
        filename = response_data["filename"]
        assert isinstance(file_path, str), "file_path must be a string"
        assert isinstance(filename, str), "filename must be a string"
        assert len(file_path) > 0, "file_path cannot be empty"
        assert len(filename) > 0, "filename cannot be empty"
        assert filename.endswith(
            f".{expected_format}"), f"filename must end with .{expected_format}"

        # Verify the file would exist in the mounted volume
        assert file_path.startswith(
            "/tmp/"), "file_path should start with /tmp/ (Docker volume mount path)"


@pytest.mark.asyncio
class AsyncMCPTest(BaseMCPTest):
    """Base class for async MCP tests using pytest."""
    pass
