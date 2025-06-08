"""
Test Kubernetes diagram generation functionality.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server, call_tool_and_verify_success, verify_diagram_response


@pytest.mark.anyio
async def test_generate_kubernetes_diagram(test_server):
    """Test generating a Kubernetes diagram."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test parameters for Kubernetes diagram
        params = {
            "title": "Test K8s Cluster"
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_kubernetes_diagram", params
        )

        await verify_diagram_response(response_data)


@pytest.mark.anyio
async def test_kubernetes_with_options(test_server):
    """Test Kubernetes diagram with various options."""
    async with client_session(test_server._mcp_server) as client:
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
        response_data = await call_tool_and_verify_success(
            client, "generate_kubernetes_diagram", params
        )

        await verify_diagram_response(response_data)


@pytest.mark.anyio
async def test_kubernetes_minimal(test_server):
    """Test Kubernetes diagram with minimal configuration."""
    async with client_session(test_server._mcp_server) as client:
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
        response_data = await call_tool_and_verify_success(
            client, "generate_kubernetes_diagram", params
        )

        await verify_diagram_response(response_data)
