"""
Test dynamic diagram ge                # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )
        await verify_diagram_response(response_data) Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )
        await verify_diagram_response(response_data, "svg") Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )
        await verify_diagram_response(response_data)ion functionality.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server, call_tool_and_verify_success, verify_diagram_response


@pytest.mark.anyio
async def test_generate_dynamic_diagram_basic(test_server):
    """Test generating a basic dynamic diagram."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test parameters for a basic dynamic diagram
        params = {
            "title": "Test Dynamic Diagram",
            "components": [
                {"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"},
                {"id": "db1", "type": "aws.database.rds", "label": "Database"}
            ],
            "connections": [
                {"from": "web1", "to": "db1", "label": "queries"}
            ]
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )
        await verify_diagram_response(response_data, "png")


@pytest.mark.anyio
async def test_generate_dynamic_diagram_custom_format(test_server):
    """Test generating a dynamic diagram with custom format."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test parameters with custom format
        params = {
            "title": "Test SVG Dynamic Diagram",
            "components": [
                {"id": "app1", "type": "aws.compute.lambda", "label": "Function"},
                {"id": "api1", "type": "aws.network.apigateway", "label": "API Gateway"}
            ],
            "connections": [
                {"from": "api1", "to": "app1", "label": "invokes"}
            ],
            "output_format": "svg"
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )
        await verify_diagram_response(response_data, "svg")


@pytest.mark.anyio
async def test_generate_dynamic_diagram_minimal_params(test_server):
    """Test generating a dynamic diagram with minimal parameters."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test with minimal required parameters
        params = {
            "title": "Minimal Dynamic Test",
            "components": [
                {"id": "single", "type": "aws.storage.s3", "label": "Storage"}
            ]
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )
        await verify_diagram_response(response_data, "png")
