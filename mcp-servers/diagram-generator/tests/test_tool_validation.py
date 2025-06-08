"""
Test tool validation and metadata.
"""

from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import AsyncMCPTest


class TestToolValidation(AsyncMCPTest):
    """Test suite for tool validation and metadata."""

    async def test_tool_descriptions(self):
        """Test that all tools have proper descriptions."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # List tools and check descriptions
            tools_result = await client.list_tools()

            for tool in tools_result.tools:
                assert tool.description is not None, f"Tool {tool.name} missing description"
                assert len(
                    tool.description) > 0, f"Tool {tool.name} has empty description"
                assert isinstance(
                    tool.description, str), f"Tool {tool.name} description is not a string"

    async def test_tool_input_schemas(self):
        """Test that all tools have proper input schemas."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # List tools and check schemas
            tools_result = await client.list_tools()

            for tool in tools_result.tools:
                assert tool.inputSchema is not None, f"Tool {tool.name} missing input schema"
                assert "type" in tool.inputSchema, f"Tool {tool.name} schema missing type"
                assert tool.inputSchema["type"] == "object", f"Tool {tool.name} schema type should be object"
                assert "properties" in tool.inputSchema, f"Tool {tool.name} schema missing properties"

    async def test_tool_parameter_validation(self):
        """Test that tools properly validate their parameters."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test each tool with valid minimal parameters
            test_cases = [
                ("generate_simple_diagram", {
                    "title": "Test",
                    "components": [{"id": "test", "type": "aws.compute.ec2", "label": "Test"}]
                }),
                ("generate_clustered_diagram", {
                    "title": "Test",
                    "clusters": [{"name": "Test", "components": [{"id": "test", "type": "aws.compute.ec2", "label": "Test"}]}]
                }),
                ("generate_aws_web_app_diagram", {
                    "title": "Test"
                }),
                ("generate_kubernetes_diagram", {
                    "title": "Test"
                }),
                ("generate_microservices_diagram", {
                    "title": "Test"
                }),
                ("list_available_components", {})
            ]

            for tool_name, params in test_cases:
                result = await client.call_tool(tool_name, params)
                assert not result.isError, f"Tool {tool_name} failed with valid parameters"

    async def test_tool_names_consistency(self):
        """Test that all expected tools are present with correct names."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            tools_result = await client.list_tools()
            tool_names = sorted([tool.name for tool in tools_result.tools])

            expected_tools = sorted([
                "generate_simple_diagram",
                "generate_clustered_diagram",
                "generate_aws_web_app_diagram",
                "generate_kubernetes_diagram",
                "generate_microservices_diagram",
                "list_available_components"
            ])

            assert tool_names == expected_tools, f"Tool names mismatch. Expected: {expected_tools}, Got: {tool_names}"
