"""
Test microservices diagram generation functionality.
"""

from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import AsyncMCPTest


class TestMicroservicesDiagrams(AsyncMCPTest):
    """Test suite for microservices diagram generation."""

    async def test_generate_microservices_diagram(self):
        """Test generating a microservices diagram."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for microservices diagram
            params = {
                "title": "Test Microservices"
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_microservices_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_microservices_with_custom_services(self):
        """Test microservices diagram with custom service list."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with custom services
            params = {
                "title": "E-commerce Microservices",
                "services": ["user-service", "product-service", "order-service", "payment-service"],
                "provider": "aws",
                "include_gateway": True,
                "include_database": True,
                "include_cache": True,
                "include_queue": True
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_microservices_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_microservices_azure_provider(self):
        """Test microservices diagram with Azure provider."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with Azure provider
            params = {
                "title": "Azure Microservices",
                "services": ["api-service", "data-service"],
                "provider": "azure",
                "include_gateway": True,
                "include_database": True,
                "include_cache": False,
                "include_queue": True
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_microservices_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_microservices_gcp_provider(self):
        """Test microservices diagram with GCP provider."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with GCP provider
            params = {
                "title": "GCP Microservices",
                "services": ["auth-service", "notification-service"],
                "provider": "gcp",
                "include_gateway": False,
                "include_database": True,
                "include_cache": True,
                "include_queue": False
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_microservices_diagram", params
            )

            await self.verify_diagram_response(response_data)
