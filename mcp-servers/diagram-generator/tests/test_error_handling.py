"""
Test error handling and edge cases.
"""

import json
import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from mcp.types import TextContent
from .base_test import test_server


@pytest.mark.anyio
async def test_error_handling_invalid_component(test_server):
    """Test error handling with invalid component types."""
    async with client_session(test_server._mcp_server) as client:
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
        result = await client.call_tool("generate_dynamic_diagram", params)

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


@pytest.mark.anyio
async def test_missing_required_parameters(test_server):
    """Test handling of missing required parameters."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test with missing title parameter
        params = {
            "components": [
                {"id": "test1", "type": "aws.compute.ec2", "label": "Test"}
            ]
        }

        # Server should return an error for missing required parameter
        result = await client.call_tool("generate_dynamic_diagram", params)

        # Verify the server returns a proper error for missing parameters
        assert result.isError  # This should be an error response
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)
        assert "Missing required argument" in result.content[0].text


@pytest.mark.anyio
async def test_empty_components_list(test_server):
    """Test handling of empty components list."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test with empty components
        params = {
            "title": "Empty Diagram",
            "components": [],
            "connections": []
        }

        # Call the tool
        result = await client.call_tool("generate_dynamic_diagram", params)

        # Verify the call doesn't crash the server
        assert not result.isError
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Parse response
        response_data = json.loads(result.content[0].text)
        assert "success" in response_data


@pytest.mark.anyio
async def test_invalid_connection_references(test_server):
    """Test handling of connections that reference non-existent components."""
    async with client_session(test_server._mcp_server) as client:
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
        result = await client.call_tool("generate_dynamic_diagram", params)

        # Verify the call doesn't crash the server
        assert not result.isError
        assert len(result.content) == 1
        assert isinstance(result.content[0], TextContent)

        # Should handle gracefully
        response_data = json.loads(result.content[0].text)
        assert "success" in response_data
