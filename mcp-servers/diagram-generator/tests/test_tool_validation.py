"""
Test tool validation and metadata.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server


@pytest.mark.anyio
async def test_tool_descriptions(test_server):
    """Test that all tools have proper descriptions."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # List tools and check descriptions
        tools_result = await client.list_tools()

        for tool in tools_result.tools:
            assert tool.description is not None, f"Tool {tool.name} missing description"
            assert len(
                tool.description) > 0, f"Tool {tool.name} has empty description"
            assert isinstance(
                tool.description, str), f"Tool {tool.name} description is not a string"


@pytest.mark.anyio
async def test_tool_input_schemas(test_server):
    """Test that all tools have proper input schemas."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # List tools and check schemas
        tools_result = await client.list_tools()

        for tool in tools_result.tools:
            assert tool.inputSchema is not None, f"Tool {tool.name} missing input schema"
            assert "type" in tool.inputSchema, f"Tool {tool.name} schema missing type"
            assert tool.inputSchema["type"] == "object", f"Tool {tool.name} schema type should be object"
            assert "properties" in tool.inputSchema, f"Tool {tool.name} schema missing properties"


@pytest.mark.anyio
async def test_tool_parameter_validation(test_server):
    """Test that tools properly validate their parameters."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test the dynamic tool with valid parameters
        test_cases = [
            ("generate_dynamic_diagram", {
                "title": "Test",
                "components": [{"id": "test", "type": "aws.compute.ec2", "label": "Test"}],
                "connections": [{"from": "test", "to": "test2", "label": "Connection"}]
            }),
            ("list_available_components", {})
        ]

        for tool_name, params in test_cases:
            result = await client.call_tool(tool_name, params)
            assert not result.isError, f"Tool {tool_name} failed with valid parameters"


@pytest.mark.anyio
async def test_tool_names_consistency(test_server):
    """Test that all expected tools are present with correct names."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        tools_result = await client.list_tools()
        tool_names = sorted([tool.name for tool in tools_result.tools])

        expected_tools = sorted([
            "generate_dynamic_diagram",
            "list_available_components"
        ])

        assert tool_names == expected_tools, f"Tool names mismatch. Expected: {expected_tools}, Got: {tool_names}"
