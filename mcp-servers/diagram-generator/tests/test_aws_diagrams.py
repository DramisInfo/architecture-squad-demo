"""
Test AWS diagram generation functionality.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server, call_tool_and_verify_success, verify_diagram_response


@pytest.mark.anyio
async def test_generate_aws_web_app_diagram(test_server):
    """Test generating an AWS web application diagram."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test parameters for AWS web app diagram
        params = {
            "title": "Test AWS Web App"
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_aws_web_app_diagram", params
        )

        await verify_diagram_response(response_data)


@pytest.mark.anyio
async def test_aws_web_app_with_options(test_server):
    """Test AWS web app diagram with various options."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test with various options enabled
        params = {
            "title": "Full AWS Web App",
            "include_cdn": True,
            "include_cache": True,
            "include_monitoring": True,
            "multi_az": True
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_aws_web_app_diagram", params
        )

        await verify_diagram_response(response_data)


@pytest.mark.anyio
async def test_aws_web_app_minimal(test_server):
    """Test AWS web app diagram with minimal configuration."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test with minimal configuration
        params = {
            "title": "Minimal AWS Web App",
            "include_cdn": False,
            "include_cache": False,
            "include_monitoring": False,
            "multi_az": False
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_aws_web_app_diagram", params
        )

        await verify_diagram_response(response_data)
