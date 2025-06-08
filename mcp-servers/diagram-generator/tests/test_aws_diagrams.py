"""
Test AWS diagram generation functionality.
"""

from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import AsyncMCPTest


class TestAWSDiagrams(AsyncMCPTest):
    """Test suite for AWS diagram generation."""

    async def test_generate_aws_web_app_diagram(self):
        """Test generating an AWS web application diagram."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for AWS web app diagram
            params = {
                "title": "Test AWS Web App"
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_aws_web_app_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_aws_web_app_with_options(self):
        """Test AWS web app diagram with various options."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
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
            response_data = await self.call_tool_and_verify_success(
                client, "generate_aws_web_app_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_aws_web_app_minimal(self):
        """Test AWS web app diagram with minimal configuration."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
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
            response_data = await self.call_tool_and_verify_success(
                client, "generate_aws_web_app_diagram", params
            )

            await self.verify_diagram_response(response_data)
