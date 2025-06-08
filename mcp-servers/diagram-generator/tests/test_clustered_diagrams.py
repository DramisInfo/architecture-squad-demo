"""
Test clustered diagram generation functionality.
"""

from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import AsyncMCPTest


class TestClusteredDiagrams(AsyncMCPTest):
    """Test suite for clustered diagram generation."""

    async def test_generate_clustered_diagram(self):
        """Test generating a clustered diagram."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test parameters for a clustered diagram
            params = {
                "title": "Test Clustered Diagram",
                "clusters": [
                    {
                        "name": "Web Tier",
                        "components": [
                            {"id": "lb1", "type": "aws.network.elb",
                                "label": "Load Balancer"}
                        ]
                    },
                    {
                        "name": "Database Tier",
                        "components": [
                            {"id": "db1", "type": "aws.database.rds",
                                "label": "Primary DB"}
                        ]
                    }
                ],
                "connections": [
                    {"from": "lb1", "to": "db1", "label": "routes"}
                ]
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_clustered_diagram", params
            )

            await self.verify_diagram_response(response_data)

    async def test_clustered_diagram_multiple_clusters(self):
        """Test generating a clustered diagram with multiple clusters."""
        mcp = self.create_test_server()

        async with client_session(mcp._mcp_server) as client:
            await client.initialize()

            # Test with multiple clusters
            params = {
                "title": "Multi-Cluster Architecture",
                "clusters": [
                    {
                        "name": "Frontend",
                        "components": [
                            {"id": "cdn1", "type": "aws.network.cloudfront",
                                "label": "CDN"},
                            {"id": "web1", "type": "aws.compute.ec2",
                                "label": "Web Server"}
                        ]
                    },
                    {
                        "name": "Backend",
                        "components": [
                            {"id": "api1", "type": "aws.compute.lambda", "label": "API"},
                            {"id": "queue1", "type": "aws.integration.sqs",
                                "label": "Queue"}
                        ]
                    },
                    {
                        "name": "Data",
                        "components": [
                            {"id": "db1", "type": "aws.database.rds",
                                "label": "Database"},
                            {"id": "cache1", "type": "aws.database.elasticache",
                                "label": "Cache"}
                        ]
                    }
                ],
                "connections": [
                    {"from": "cdn1", "to": "web1", "label": "serves"},
                    {"from": "web1", "to": "api1", "label": "calls"},
                    {"from": "api1", "to": "queue1", "label": "enqueues"},
                    {"from": "api1", "to": "db1", "label": "queries"},
                    {"from": "api1", "to": "cache1", "label": "caches"}
                ]
            }

            # Call the tool and verify response
            response_data = await self.call_tool_and_verify_success(
                client, "generate_clustered_diagram", params
            )

            await self.verify_diagram_response(response_data)
