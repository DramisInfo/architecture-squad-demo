"""
Test edge cases and error handling for the Diagram Generator MCP server.

This module tests various edge cases, error conditions, and boundary scenarios
for the component validation and diagram generation functionality.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as client_session
from .base_test import test_server, call_tool_and_verify_success


@pytest.mark.anyio
async def test_component_validation_stress_test(test_server):
    """Test validation with a large number of components."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        # Create a large number of valid components
        components = []
        for i in range(50):
            components.append({
                "id": f"component_{i}",
                "type": "aws.compute.ec2",
                "label": f"Server {i}"
            })

        params = {
            "title": "Stress Test Diagram",
            "components": components
        }

        # This should succeed even with many components
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        assert response_data["components_count"] == 50
        assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_component_validation_special_characters(test_server):
    """Test validation with special characters in component IDs and labels."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Special Characters Test",
            "components": [
                {"id": "comp-with-hyphens", "type": "aws.compute.ec2",
                    "label": "Server with-hyphens"},
                {"id": "comp_with_underscores", "type": "aws.database.rds",
                    "label": "DB_with_underscores"},
                {"id": "comp123", "type": "k8s.compute.pod", "label": "Pod 123"},
                {"id": "comp.with.dots", "type": "azure.compute.vm",
                    "label": "VM with spaces"}
            ]
        }

        # This should succeed with special characters in IDs and labels
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        assert response_data["components_count"] == 4
        assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_component_validation_unicode_characters(test_server):
    """Test validation with Unicode characters in labels."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Unicode Test 测试",
            "components": [
                {"id": "unicode1", "type": "aws.compute.ec2", "label": "服务器 Server"},
                {"id": "unicode2", "type": "aws.database.rds",
                    "label": "数据库 Database"},
                {"id": "unicode3", "type": "k8s.compute.pod", "label": "Pod 🚀"},
                {"id": "unicode4", "type": "azure.compute.vm", "label": "VM ñáéíóú"}
            ]
        }

        # This should succeed with Unicode characters
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        assert response_data["components_count"] == 4
        assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_component_validation_case_sensitivity(test_server):
    """Test that component validation is case-sensitive."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Case Sensitivity Test",
            "components": [
                {"id": "case1", "type": "AWS.COMPUTE.EC2", "label": "Uppercase"},
                {"id": "case2", "type": "aws.Compute.Ec2", "label": "Mixed Case"},
                {"id": "case3", "type": "aws.compute.EC2",
                    "label": "Component Uppercase"}
            ]
        }

        result = await client.call_tool("generate_dynamic_diagram", params)

        import json
        response_data = json.loads(result.content[0].text)

        # Should fail because component types are case-sensitive
        assert response_data["success"] is False
        assert "Component validation failed" in response_data["error"]
        assert len(response_data["details"]) == 3  # All should be invalid


@pytest.mark.anyio
async def test_component_validation_duplicate_ids(test_server):
    """Test behavior with duplicate component IDs."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Duplicate IDs Test",
            "components": [
                {"id": "duplicate", "type": "aws.compute.ec2",
                    "label": "First Server"},
                {"id": "duplicate", "type": "aws.database.rds",
                    "label": "Second Database"},
                {"id": "unique", "type": "k8s.compute.pod", "label": "Unique Pod"}
            ]
        }

        # This should still validate (validation doesn't check for duplicate IDs)
        # but may have unexpected behavior in diagram generation
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        assert response_data["components_count"] == 3
        assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_component_validation_extra_fields(test_server):
    """Test validation with extra fields in component definitions."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Extra Fields Test",
            "components": [
                {
                    "id": "extra1",
                    "type": "aws.compute.ec2",
                    "label": "Server with extras",
                    "description": "This is a description",
                    "cost": 100,
                    "tags": ["web", "production"]
                },
                {
                    "id": "extra2",
                    "type": "aws.database.rds",
                    "label": "Database",
                    "engine": "postgresql",
                    "version": "13.7"
                }
            ]
        }

        # This should succeed (extra fields should be ignored)
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        assert response_data["components_count"] == 2
        assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_connections_with_invalid_component_ids(test_server):
    """Test connections referencing non-existent component IDs."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Invalid Connection IDs Test",
            "components": [
                {"id": "valid1", "type": "aws.compute.ec2", "label": "Valid Server"},
                {"id": "valid2", "type": "aws.database.rds",
                    "label": "Valid Database"}
            ],
            "connections": [
                {"from": "valid1", "to": "valid2", "label": "valid connection"},
                {"from": "valid1", "to": "nonexistent",
                    "label": "invalid connection"},
                {"from": "another_nonexistent",
                    "to": "valid2", "label": "another invalid"}
            ]
        }

        # Should succeed but log warnings about invalid connections
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        assert response_data["components_count"] == 2
        # All connections are counted
        assert response_data["connections_count"] == 3
        assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_different_output_formats_validation(test_server):
    """Test validation works with different output formats."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        for output_format in ["png", "svg", "pdf", "jpg"]:
            params = {
                "title": f"Format Test {output_format.upper()}",
                "components": [
                    {"id": "test1", "type": "aws.compute.ec2", "label": "Test Server"}
                ],
                "output_format": output_format
            }

            response_data = await call_tool_and_verify_success(
                client, "generate_dynamic_diagram", params
            )

            assert response_data["format"] == output_format
            assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_different_directions_validation(test_server):
    """Test validation works with different diagram directions."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        for direction in ["TB", "BT", "LR", "RL"]:
            params = {
                "title": f"Direction Test {direction}",
                "components": [
                    {"id": "test1", "type": "aws.compute.ec2", "label": "Test Server"}
                ],
                "direction": direction
            }

            response_data = await call_tool_and_verify_success(
                client, "generate_dynamic_diagram", params
            )

            assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_validation_error_details_comprehensive(test_server):
    """Test that validation error details are comprehensive and helpful."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Comprehensive Error Test",
            "components": [
                {"id": "error1", "type": "nonexistent.provider.server",
                    "label": "Bad Provider"},
                {"id": "error2", "type": "aws.badcategory.server",
                    "label": "Bad Category"},
                {"id": "error3", "type": "aws.compute.badcomponent",
                    "label": "Bad Component"},
                {"id": "error4", "type": "malformed", "label": "Malformed Type"},
                {"id": "error5", "type": "also.malformed",
                    "label": "Also Malformed"},
                {"id": "valid1", "type": "aws.compute.ec2",
                    "label": "Valid Component"}
            ]
        }

        result = await client.call_tool("generate_dynamic_diagram", params)

        import json
        response_data = json.loads(result.content[0].text)

        # Verify comprehensive error reporting
        assert response_data["success"] is False
        assert "Component validation failed" in response_data["error"]
        assert len(response_data["details"]) == 5  # 5 invalid components

        # Check validation info
        assert response_data["validation_info"]["total_components"] == 6
        assert response_data["validation_info"]["valid_components"] == 1
        assert response_data["validation_info"]["invalid_components"] == 5

        # Verify each error has helpful details
        error_types = set()
        for detail in response_data["details"]:
            assert "id" in detail
            assert "type" in detail
            assert "error" in detail
            error_types.add(detail["type"])

        # Verify we have the expected error types
        expected_types = {
            "nonexistent.provider.server",
            "aws.badcategory.server",
            "aws.compute.badcomponent",
            "malformed",
            "also.malformed"
        }
        assert error_types == expected_types


@pytest.mark.anyio
async def test_empty_connections_list(test_server):
    """Test behavior with empty connections list."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "Empty Connections Test",
            "components": [
                {"id": "standalone1", "type": "aws.compute.ec2",
                    "label": "Standalone Server"},
                {"id": "standalone2", "type": "aws.database.rds",
                    "label": "Standalone Database"}
            ],
            "connections": []
        }

        # Should succeed with empty connections
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        assert response_data["components_count"] == 2
        assert response_data["connections_count"] == 0
        assert response_data["validation_info"]["all_components_valid"] is True


@pytest.mark.anyio
async def test_no_connections_parameter(test_server):
    """Test behavior when connections parameter is not provided."""
    async with client_session(test_server._mcp_server) as client:
        await client.initialize()

        params = {
            "title": "No Connections Parameter Test",
            "components": [
                {"id": "isolated1", "type": "aws.compute.ec2",
                    "label": "Isolated Server"},
                {"id": "isolated2", "type": "aws.database.rds",
                    "label": "Isolated Database"}
            ]
            # No connections parameter at all
        }

        # Should succeed without connections parameter
        response_data = await call_tool_and_verify_success(
            client, "generate_dynamic_diagram", params
        )

        assert response_data["components_count"] == 2
        assert response_data["connections_count"] == 0
        assert response_data["validation_info"]["all_components_valid"] is True
