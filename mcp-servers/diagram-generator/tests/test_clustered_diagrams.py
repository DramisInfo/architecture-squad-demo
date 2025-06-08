"""
Test clustered diagram ge        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        await verify_diagram_response(response_data)on functionality.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server, call_tool_and_verify_success, verify_diagram_response


@pytest.mark.anyio
async def test_generate_clustered_diagram(test_server):
    """Test generating a clustered diagram."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test parameters for a clustered diagram
        params = {
            "title": "Test Clustered Diagram",
            "components": [
                {"id": "comp1", "type": "aws.compute.ec2", "label": "Web Server"},
                {"id": "comp2", "type": "aws.database.rds", "label": "Database"},
                {"id": "comp3", "type": "aws.storage.s3", "label": "Storage"}
            ],
            "connections": [
                {"from": "comp1", "to": "comp2", "label": "queries"},
                {"from": "comp1", "to": "comp3", "label": "stores"}
            ]
        }

        # Call the tool and verify response
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        await verify_diagram_response(response_data, "png")
