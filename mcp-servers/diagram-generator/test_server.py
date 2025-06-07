"""
Official MCP SDK test for the Diagram Generator MCP server.

This test follows the official MCP Python SDK testing patterns found in:
- https://github.com/modelcontextprotocol/python-sdk/tree/main/tests/
"""

import asyncio
import base64
import json
import tempfile
from pathlib import Path

import pytest

from mcp.server.fastmcp import FastMCP
from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
from mcp.types import TextContent


# Import the server (assuming it can be imported)
def create_test_server() -> FastMCP:
    """Create the diagram generator MCP server for testing."""
    # Import the server from the local module
    import sys
    sys.path.append(str(Path(__file__).parent))

    from server import mcp
    return mcp


@pytest.mark.asyncio
class TestDiagramGeneratorMCP:
    """Test suite for the Diagram Generator MCP server."""

    async def test_server_initialization(self):
        """Test that the server initializes correctly."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            # Test initialization
            result = await client.initialize()
            assert result.serverInfo.name == "Diagram Generator Server"

            # Verify server capabilities
            assert result.capabilities.tools is not None
            assert result.capabilities.tools.listChanged is False  # Default FastMCP behavior

    async def test_list_tools(self):
        """Test that all expected tools are available."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
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

    async def test_list_available_components(self):
        """Test the list_available_components tool."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Call the list_available_components tool
            result = await client.call_tool("list_available_components", {})

            # Verify successful execution
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Parse the JSON response
            component_data = json.loads(result.content[0].text)
            assert "success" in component_data
            assert component_data["success"] is True
            assert "components" in component_data

            # Verify expected component categories
            components = component_data["components"]
            expected_categories = ["aws", "azure", "gcp", "k8s", "onprem"]
            for category in expected_categories:
                assert category in components

    async def test_generate_simple_diagram(self):
        """Test generating a simple diagram."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for a simple diagram
            params = {
                "title": "Test Simple Diagram",
                "components": [
                    {"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"},
                    {"id": "db1", "type": "aws.database.rds", "label": "Database"}
                ],
                "connections": [
                    {"from": "web1", "to": "db1", "label": "queries"}
                ]
            }

            # Call the tool
            result = await client.call_tool("generate_simple_diagram", params)

            # Verify successful execution
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Parse the response
            response_data = json.loads(result.content[0].text)
            assert "success" in response_data
            assert response_data["success"] is True
            assert "image_base64" in response_data
            assert "format" in response_data
            assert response_data["format"] == "png"

            # Verify base64 data is valid
            # Changed from diagram_base64
            diagram_data = response_data["image_base64"]
            assert isinstance(diagram_data, str)
            assert len(diagram_data) > 0

            # Test that base64 can be decoded
            try:
                decoded_data = base64.b64decode(diagram_data)
                assert len(decoded_data) > 0
            except Exception as e:
                pytest.fail(f"Invalid base64 data: {e}")

    async def test_generate_clustered_diagram(self):
        """Test generating a clustered diagram."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for a clustered diagram
            params = {
                "title": "Test Clustered Diagram",
                "clusters": [
                    {
                        "name": "Web Tier",
                        "components": [
                            {"id": "lb1", "type": "aws.network.elb",
                                "label": "Load Balancer"}
                        ]
                    },
                    {
                        "name": "Database Tier",
                        "components": [
                            {"id": "db1", "type": "aws.database.rds",
                                "label": "Primary DB"}
                        ]
                    }
                ],
                "connections": [
                    {"from": "lb1", "to": "db1", "label": "routes"}
                ]
            }

            # Call the tool
            result = await client.call_tool("generate_clustered_diagram", params)

            # Verify successful execution
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Parse the response
            response_data = json.loads(result.content[0].text)
            assert response_data["success"] is True
            assert "image_base64" in response_data
            assert "format" in response_data

    async def test_generate_aws_web_app_diagram(self):
        """Test generating an AWS web application diagram."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for AWS web app diagram
            params = {
                "title": "Test Web App"
            }

            # Call the tool
            result = await client.call_tool("generate_aws_web_app_diagram", params)

            # Verify successful execution
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Parse the response
            response_data = json.loads(result.content[0].text)
            assert response_data["success"] is True
            assert "image_base64" in response_data
            assert "format" in response_data

    async def test_generate_kubernetes_diagram(self):
        """Test generating a Kubernetes diagram."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for Kubernetes diagram
            params = {
                "title": "Test Cluster"
            }

            # Call the tool
            result = await client.call_tool("generate_kubernetes_diagram", params)

            # Verify successful execution
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Parse the response
            response_data = json.loads(result.content[0].text)
            assert response_data["success"] is True
            assert "image_base64" in response_data
            assert "format" in response_data

    async def test_generate_microservices_diagram(self):
        """Test generating a microservices diagram."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for microservices diagram
            params = {
                "title": "Test Microservices"
            }

            # Call the tool
            result = await client.call_tool("generate_microservices_diagram", params)

            # Verify successful execution
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Parse the response
            response_data = json.loads(result.content[0].text)
            assert response_data["success"] is True
            assert "image_base64" in response_data
            assert "format" in response_data

    async def test_error_handling_invalid_component(self):
        """Test error handling with invalid component types."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with invalid component type
            params = {
                "title": "Test Error",
                "components": [
                    {"id": "invalid1", "type": "invalid_provider.compute.nonexistent",
                        "label": "Invalid"}
                ],
                "connections": []
            }

            # Call the tool - should handle error gracefully
            result = await client.call_tool("generate_simple_diagram", params)

            # Verify the call doesn't crash the server
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Parse response - could be success or error, but should be valid JSON
            response_data = json.loads(result.content[0].text)
            assert "success" in response_data
            assert isinstance(response_data["success"], bool)

            # If it fails, should have error message
            if response_data["success"] is False:
                assert "error" in response_data

    async def test_tool_descriptions(self):
        """Test that all tools have proper descriptions."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # List tools and check descriptions
            tools_result = await client.list_tools()

            for tool in tools_result.tools:
                assert tool.description is not None
                assert len(tool.description) > 0
                assert isinstance(tool.description, str)

    async def test_tool_input_schemas(self):
        """Test that all tools have proper input schemas."""
        mcp = create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # List tools and check schemas
            tools_result = await client.list_tools()

            for tool in tools_result.tools:
                assert tool.inputSchema is not None
                assert "type" in tool.inputSchema
                assert tool.inputSchema["type"] == "object"
                assert "properties" in tool.inputSchema


if __name__ == "__main__":
    """Run the tests directly for development."""
    async def run_tests():
        """Run all tests for the MCP diagram generator server."""
        print("🧪 Testing Diagram Generator MCP Server...")

        test_instance = TestDiagramGeneratorMCP()

        try:
            print("✅ Testing server initialization...")
            await test_instance.test_server_initialization()

            print("✅ Testing tool listing...")
            await test_instance.test_list_tools()

            print("✅ Testing component listing...")
            await test_instance.test_list_available_components()

            print("✅ Testing simple diagram generation...")
            await test_instance.test_generate_simple_diagram()

            print("✅ Testing clustered diagram generation...")
            await test_instance.test_generate_clustered_diagram()

            print("✅ Testing AWS web app diagram...")
            await test_instance.test_generate_aws_web_app_diagram()

            print("✅ Testing Kubernetes diagram...")
            await test_instance.test_generate_kubernetes_diagram()

            print("✅ Testing microservices diagram...")
            await test_instance.test_generate_microservices_diagram()

            print("✅ Testing error handling...")
            await test_instance.test_error_handling_invalid_component()

            print("✅ Testing tool descriptions...")
            await test_instance.test_tool_descriptions()

            print("✅ Testing tool schemas...")
            await test_instance.test_tool_input_schemas()

            print("🎉 All tests passed!")

        except Exception as e:
            print(f"❌ Test failed: {e}")
            raise

    # Run the tests
    asyncio.run(run_tests())
