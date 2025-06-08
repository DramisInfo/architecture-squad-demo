"""
Test error handling and edge cases.
"""

import json
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from mcp.types import TextContent
from .base_test import AsyncMCPTest


class TestErrorHandling(AsyncMCPTest):
    """Test suite for error handling and edge cases."""

    async def test_error_handling_invalid_component(self):
        """Test error handling with invalid component types."""
        mcp = self.create_test_server()

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

    async def test_missing_required_parameters(self):
        """Test handling of missing required parameters."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with missing title parameter
            params = {
                "components": [
                    {"id": "test1", "type": "aws.compute.ec2", "label": "Test"}
                ]
            }

            # This should fail gracefully or use a default title
            result = await client.call_tool("generate_simple_diagram", params)

            # Verify the call doesn't crash the server
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

    async def test_empty_components_list(self):
        """Test handling of empty components list."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with empty components
            params = {
                "title": "Empty Diagram",
                "components": [],
                "connections": []
            }

            # Call the tool
            result = await client.call_tool("generate_simple_diagram", params)

            # Verify the call doesn't crash the server
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Parse response
            response_data = json.loads(result.content[0].text)
            assert "success" in response_data

    async def test_invalid_connection_references(self):
        """Test handling of connections that reference non-existent components."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with connection referencing non-existent component
            params = {
                "title": "Invalid Connection Test",
                "components": [
                    {"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"}
                ],
                "connections": [
                    {"from": "web1", "to": "nonexistent", "label": "invalid"}
                ]
            }

            # Call the tool
            result = await client.call_tool("generate_simple_diagram", params)

            # Verify the call doesn't crash the server
            assert not result.isError
            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)

            # Should handle gracefully
            response_data = json.loads(result.content[0].text)
            assert "success" in response_data
