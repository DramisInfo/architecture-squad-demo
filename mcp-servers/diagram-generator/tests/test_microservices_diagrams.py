"""
Test microservices diagram generation functionality.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server, call_tool_and_verify_success, verify_diagram_response


@pytest.mark.anyio
async def test_generate_microservices_diagram(test_server):
    """Test generating a microservices diagram."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test parameters for microservices diagram
        params = {
            "title": "Test Microservices"
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_microservices_diagram", params
        )

        await verify_diagram_response(response_data)


@pytest.mark.anyio
async def test_microservices_with_custom_services(test_server):
    """Test microservices diagram with custom service list."""
    async with client_session(test_server._mcp_server) as client:
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
        response_data = await call_tool_and_verify_success(
            client, "generate_microservices_diagram", params
        )

        await verify_diagram_response(response_data)


@pytest.mark.anyio
async def test_microservices_azure_provider(test_server):
    """Test microservices diagram with Azure provider."""
    async with client_session(test_server._mcp_server) as client:
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
        response_data = await call_tool_and_verify_success(
            client, "generate_microservices_diagram", params
        )

        await verify_diagram_response(response_data)


@pytest.mark.anyio
async def test_microservices_gcp_provider(test_server):
    """Test microservices diagram with GCP provider."""
    async with client_session(test_server._mcp_server) as client:
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
        response_data = await call_tool_and_verify_success(
            client, "generate_microservices_diagram", params
        )

        await verify_diagram_response(response_data)
