"""
Test Kubernetes diagram generation functionality.
"""

from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import AsyncMCPTest


class TestKubernetesDiagrams(AsyncMCPTest):
    """Test suite for Kubernetes diagram generation."""

    async def test_generate_kubernetes_diagram(self):
        """Test generating a Kubernetes diagram."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for Kubernetes diagram
            params = {
                "title": "Test K8s Cluster"
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_kubernetes_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_kubernetes_with_options(self):
        """Test Kubernetes diagram with various options."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with various options
            params = {
                "title": "Full K8s Architecture",
                "replicas": 5,
                "include_ingress": True,
                "include_hpa": True,
                "include_storage": True
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_kubernetes_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_kubernetes_minimal(self):
        """Test Kubernetes diagram with minimal configuration."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with minimal configuration
            params = {
                "title": "Simple K8s Setup",
                "replicas": 1,
                "include_ingress": False,
                "include_hpa": False,
                "include_storage": False
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_kubernetes_diagram", params
            )

            await self.verify_diagram_response(response_data)
