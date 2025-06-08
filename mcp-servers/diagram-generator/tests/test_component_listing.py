"""
Test component listing functionality.
"""

import json
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import AsyncMCPTest


class TestComponentListing(AsyncMCPTest):
    """Test suite for component listing functionality."""

    async def test_list_available_components(self):
        """Test the list_available_components tool."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Call the list_available_components tool
            response_data = await self.call_tool_and_verify_success(
                client, "list_available_components", {}
            )

            assert "components" in response_data, "Response missing components field"

            # Verify expected component categories
            components = response_data["components"]
            expected_categories = ["aws", "azure", "gcp", "k8s", "onprem"]
            for category in expected_categories:
                assert category in components, f"Missing component category: {category}"
