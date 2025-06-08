"""
Test component validation functionality in the Diagram Generator MCP server.

This module tests the validate_components function and its integration with
the generate_dynamic_diagram tool.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server, call_tool_and_verify_success


@pytest.mark.anyio
async def test_validate_components_all_valid(test_server):
    """Test validation with all valid components."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Test with valid components from different providers
        params = {
            "title": "Valid Components Test",
            "components": [
                {"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"},
                {"id": "db1", "type": "aws.database.rds", "label": "Database"},
                {"id": "k8s_pod", "type": "k8s.compute.pod",
                    "label": "Kubernetes Pod"},
                {"id": "azure_vm", "type": "azure.compute.vm", "label": "Azure VM"}
            ]
        }

        # This should succeed since all components are valid
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        # Verify validation info is included
        assert "validation_info" in response_data
        assert response_data["validation_info"]["all_components_valid"] is True
        assert response_data["validation_info"]["total_components"] == 4


@pytest.mark.anyio
async def test_validate_components_invalid_provider(test_server):
    """Test validation with invalid provider."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Invalid Provider Test",
            "components": [
                {"id": "invalid1", "type": "invalid_provider.compute.server",
                    "label": "Invalid Server"}
            ]
        }

        # Call the tool and expect validation failure
        result = await client.call_tool("generate_dynamic_diagram", params)

        # Should not return an error at the MCP level, but should indicate failure in the response
        assert not result.isError, "Tool should not return MCP error for validation failure"

        import json
        response_data = json.loads(result.content[0].text)

        # Verify validation failure
        assert response_data["success"] is False
        assert "Component validation failed" in response_data["error"]
        assert "details" in response_data
        assert len(response_data["details"]) == 1
        assert "Unknown provider 'invalid_provider'" in response_data["details"][0]["error"]


@pytest.mark.anyio
async def test_validate_components_invalid_category(test_server):
    """Test validation with invalid category."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Invalid Category Test",
            "components": [
                {"id": "invalid1", "type": "aws.invalid_category.server",
                    "label": "Invalid Category"}
            ]
        }

        result = await client.call_tool("generate_dynamic_diagram", params)

        import json
        response_data = json.loads(result.content[0].text)

        # Verify validation failure
        assert response_data["success"] is False
        assert "Component validation failed" in response_data["error"]
        assert "Unknown category 'invalid_category'" in response_data["details"][0]["error"]


@pytest.mark.anyio
async def test_validate_components_invalid_component(test_server):
    """Test validation with invalid component name."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Invalid Component Test",
            "components": [
                {"id": "invalid1", "type": "aws.compute.invalid_component",
                    "label": "Invalid Component"}
            ]
        }

        result = await client.call_tool("generate_dynamic_diagram", params)

        import json
        response_data = json.loads(result.content[0].text)

        # Verify validation failure
        assert response_data["success"] is False
        assert "Component validation failed" in response_data["error"]
        assert "Unknown component 'invalid_component'" in response_data["details"][0]["error"]


@pytest.mark.anyio
async def test_validate_components_invalid_format(test_server):
    """Test validation with invalid component type format."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Invalid Format Test",
            "components": [
                {"id": "invalid1", "type": "aws.compute",
                    "label": "Missing Component Name"},
                {"id": "invalid2", "type": "aws",
                    "label": "Missing Category and Component"},
                {"id": "invalid3", "type": "", "label": "Empty Type"}
            ]
        }

        result = await client.call_tool("generate_dynamic_diagram", params)

        import json
        response_data = json.loads(result.content[0].text)

        # Verify validation failure
        assert response_data["success"] is False
        assert "Component validation failed" in response_data["error"]
        assert len(response_data["details"]) == 3

        # Check that all format errors are detected
        for detail in response_data["details"]:
            assert "Invalid component type format" in detail["error"]


@pytest.mark.anyio
async def test_validate_components_mixed_valid_invalid(test_server):
    """Test validation with mix of valid and invalid components."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Mixed Valid/Invalid Test",
            "components": [
                {"id": "valid1", "type": "aws.compute.ec2", "label": "Valid EC2"},
                {"id": "invalid1", "type": "invalid.provider.server",
                    "label": "Invalid Provider"},
                {"id": "valid2", "type": "k8s.compute.pod", "label": "Valid Pod"},
                {"id": "invalid2", "type": "aws.invalid.component",
                    "label": "Invalid Category"}
            ]
        }

        result = await client.call_tool("generate_dynamic_diagram", params)

        import json
        response_data = json.loads(result.content[0].text)

        # Verify validation failure
        assert response_data["success"] is False
        assert "Component validation failed" in response_data["error"]
        assert len(response_data["details"]) == 2  # Two invalid components

        # Verify validation info
        assert "validation_info" in response_data
        assert response_data["validation_info"]["total_components"] == 4
        assert response_data["validation_info"]["valid_components"] == 2
        assert response_data["validation_info"]["invalid_components"] == 2


@pytest.mark.anyio
async def test_validate_components_empty_list(test_server):
    """Test validation with empty components list."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Empty Components Test",
            "components": []
        }

        result = await client.call_tool("generate_dynamic_diagram", params)

        import json
        response_data = json.loads(result.content[0].text)

        # Verify failure due to empty components
        assert response_data["success"] is False
        assert "Components list cannot be empty" in response_data["error"]


@pytest.mark.anyio
async def test_validate_components_missing_fields(test_server):
    """Test validation with components missing required fields."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Missing Fields Test",
            "components": [
                {"id": "missing_type", "label": "No Type Field"},
                {"type": "aws.compute.ec2", "label": "No ID Field"},
                {"id": "valid", "type": "aws.compute.ec2",
                    "label": "Valid Component"}
            ]
        }

        result = await client.call_tool("generate_dynamic_diagram", params)

        import json
        response_data = json.loads(result.content[0].text)

        # Should fail validation due to missing type field
        assert response_data["success"] is False
        assert "Component validation failed" in response_data["error"]


@pytest.mark.anyio
async def test_validate_kubernetes_components_comprehensive(test_server):
    """Test validation with comprehensive Kubernetes components."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Kubernetes Comprehensive Test",
            "components": [
                {"id": "pod1", "type": "k8s.compute.pod", "label": "Pod"},
                {"id": "deployment1", "type": "k8s.compute.deployment",
                    "label": "Deployment"},
                {"id": "service1", "type": "k8s.network.service", "label": "Service"},
                {"id": "ingress1", "type": "k8s.network.ingress", "label": "Ingress"},
                {"id": "pv1", "type": "k8s.storage.pv",
                    "label": "Persistent Volume"},
                {"id": "hpa1", "type": "k8s.config.hpa", "label": "HPA"}
            ],
            "connections": [
                {"from": "ingress1", "to": "service1", "label": "routes"},
                {"from": "service1", "to": "pod1", "label": "forwards"},
                {"from": "pod1", "to": "pv1", "label": "mounts"}
            ]
        }

        # This should succeed with all valid Kubernetes components
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        # Verify all components were processed
        assert response_data["components_count"] == 6
        assert response_data["connections_count"] == 3
        assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_validate_multi_provider_architecture(test_server):
    """Test validation with multi-provider architecture."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Multi-Provider Architecture",
            "components": [
                # AWS components
                {"id": "aws_lb", "type": "aws.network.elb",
                    "label": "AWS Load Balancer"},
                {"id": "aws_ec2", "type": "aws.compute.ec2", "label": "AWS EC2"},
                {"id": "aws_rds", "type": "aws.database.rds", "label": "AWS RDS"},

                # Azure components
                {"id": "azure_vm", "type": "azure.compute.vm", "label": "Azure VM"},
                {"id": "azure_sql", "type": "azure.database.sql", "label": "Azure SQL"},

                # Kubernetes components
                {"id": "k8s_pod", "type": "k8s.compute.pod", "label": "K8s Pod"},
                {"id": "k8s_svc", "type": "k8s.network.service",
                    "label": "K8s Service"},

                # On-premises components
                {"id": "onprem_server", "type": "onprem.compute.server",
                    "label": "On-Prem Server"},
                {"id": "onprem_db", "type": "onprem.database.postgresql",
                    "label": "PostgreSQL"}
            ],
            "connections": [
                {"from": "aws_lb", "to": "aws_ec2", "label": "balances"},
                {"from": "aws_ec2", "to": "aws_rds", "label": "queries"},
                {"from": "azure_vm", "to": "azure_sql", "label": "connects"},
                {"from": "k8s_svc", "to": "k8s_pod", "label": "routes"}
            ]
        }

        # This should succeed with components from multiple providers
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        # Verify all components were processed correctly
        assert response_data["components_count"] == 9
        assert response_data["connections_count"] == 4
        assert response_data["validation_info"]["all_components_valid"] is True
        assert response_data["validation_info"]["total_components"] == 9
