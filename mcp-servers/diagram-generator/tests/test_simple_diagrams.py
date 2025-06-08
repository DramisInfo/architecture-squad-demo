"""
Test simple diagram generation functionality.
"""

from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import AsyncMCPTest


class TestSimpleDiagrams(AsyncMCPTest):
    """Test suite for simple diagram generation."""

    async def test_generate_simple_diagram(self):
        """Test generating a simple diagram."""
        mcp = self.create_test_server()

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

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_simple_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_simple_diagram_with_custom_format(self):
        """Test generating a simple diagram with custom format."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters with custom format
            params = {
                "title": "Test SVG Diagram",
                "components": [
                    {"id": "app1", "type": "aws.compute.lambda", "label": "Function"}
                ],
                "connections": [],
                "output_format": "svg"
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_simple_diagram", params
            )

            await self.verify_diagram_response(response_data, expected_format="svg")

    async def test_simple_diagram_minimal_params(self):
        """Test generating a simple diagram with minimal parameters."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with minimal required parameters
            params = {
                "title": "Minimal Test",
                "components": [
                    {"id": "single", "type": "aws.storage.s3", "label": "Storage"}
                ]
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_simple_diagram", params
            )

            await self.verify_diagram_response(response_data)
