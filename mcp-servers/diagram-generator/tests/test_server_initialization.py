"""
Test server initialization and basic functionality.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server


@pytest.mark.anyio
async def test_server_initialization(test_server):
    """Test that the server initializes correctly."""
    async with client_session(test_server._mcp_server) as client:
        # Test initialization
        result = await client.initialize()
        assert result.serverInfo.name == "Diagram Generator Server"

        # Verify server capabilities
        assert result.capabilities.tools is not None
        assert result.capabilities.tools.listChanged is False  # Default FastMCP behavior


@pytest.mark.anyio
async def test_list_tools(test_server):
    """Test that all expected tools are available."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # List available tools
        tools_result = await client.list_tools()
        tool_names = [tool.name for tool in tools_result.tools]

        # Verify all expected tools are present
        expected_tools = [
            "generate_simple_diagram",
            "generate_clustered_diagram",
            "generate_aws_web_app_diagram",
            "generate_kubernetes_diagram",
            "generate_microservices_diagram",
            "list_available_components"
        ]

        for expected_tool in expected_tools:
            assert expected_tool in tool_names, f"Tool {expected_tool} not found"
