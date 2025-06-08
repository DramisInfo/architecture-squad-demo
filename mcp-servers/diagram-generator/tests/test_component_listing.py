"""
Test component listing functionality.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server, call_tool_and_verify_success


@pytest.mark.anyio
async def test_list_available_components(test_server):
    """Test the list_available_components tool."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Call the list_available_components tool
        response_data = await call_tool_and_verify_success(
            client, "list_available_components", {}
        )

        assert "components" in response_data, "Response missing components field"

        # Verify expected component categories
        components = response_data["components"]
        expected_categories = ["aws", "azure", "gcp", "k8s", "onprem"]
        for category in expected_categories:
            assert category in components, f"Missing component category: {category}"
