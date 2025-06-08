#!/usr/bin/env python3
"""
Main MCP Server for Architecture Diagram Generator

This MCP server provides tools for generating architecture diagrams using the diagrams library.
It supports AWS, Azure, GCP, Kubernetes, and On-Premises components.
"""

from diagram_generators.clustered_diagram import generate_diagram as generate_dynamic_diagram
from fastmcp import FastMCP
from core.config import logger

from core.utils import list_available_components, generate_unique_filename, get_component_class
from typing import List, Dict, Any
from diagrams import Diagram, Edge, Cluster
import os

# Create MCP server
mcp = FastMCP("Diagram Generator Server")

# Register all tools with the MCP server
mcp.tool()(list_available_components)


def validate_components(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate that all requested components are available.

    Args:
        components: List of component specifications

    Returns:
        Dict with validation results
    """
    try:
        # Get all available components
        available_data = list_available_components()
        if not available_data["success"]:
            return {
                "valid": False,
                "error": "Failed to retrieve available components",
                "details": available_data.get("error", "Unknown error")
            }

        available_components = available_data["components"]
        invalid_components = []

        for comp in components:
            comp_type = comp.get("type", "")
            comp_id = comp.get("id", "unknown")

            # Parse component type (provider.category.component)
            parts = comp_type.split(".")
            if len(parts) != 3:
                invalid_components.append({
                    "id": comp_id,
                    "type": comp_type,
                    "error": f"Invalid component type format. Expected 'provider.category.component', got '{comp_type}'"
                })
                continue

            provider, category, component = parts

            # Check if provider exists
            if provider not in available_components:
                invalid_components.append({
                    "id": comp_id,
                    "type": comp_type,
                    "error": f"Unknown provider '{provider}'. Available providers: {list(available_components.keys())}"
                })
                continue

            # Check if category exists for the provider
            if category not in available_components[provider]:
                invalid_components.append({
                    "id": comp_id,
                    "type": comp_type,
                    "error": f"Unknown category '{category}' for provider '{provider}'. Available categories: {list(available_components[provider].keys())}"
                })
                continue

            # Check if component exists in the category
            if component not in available_components[provider][category]:
                invalid_components.append({
                    "id": comp_id,
                    "type": comp_type,
                    "error": f"Unknown component '{component}' in '{provider}.{category}'. Available components: {available_components[provider][category]}"
                })
                continue

        if invalid_components:
            return {
                "valid": False,
                "error": f"Found {len(invalid_components)} invalid component(s)",
                "invalid_components": invalid_components,
                "total_components": len(components),
                "valid_components": len(components) - len(invalid_components)
            }

        return {
            "valid": True,
            "message": f"All {len(components)} components are valid",
            "total_components": len(components)
        }

    except Exception as e:
        logger.error(f"Error validating components: {str(e)}")
        return {
            "valid": False,
            "error": f"Component validation failed: {str(e)}"
        }


async def generate_dynamic_diagram(
    title: str,
    components: List[Dict[str, Any]],
    connections: List[Dict[str, Any]] = None,
    clusters: List[Dict[str, Any]] = None,
    output_format: str = "png",
    direction: str = "TB"
) -> Dict[str, Any]:
    """
    Generate a dynamic architecture diagram based on provided components and connections.

    Args:
        title: The title of the diagram
        components: List of components in JSON format. Each component should follow this schema:
            {
                "id": "unique_identifier",  # Unique identifier for the component
                "type": "provider.category.component",  # Component type in the format 'provider.category.component'
                "label": "optional_label",  # Optional label for the component
                "cluster": "cluster_id"  # Optional cluster ID to group this component
            }
            Refer to the `list_available_components` tool to get the full list of supported components.
        connections: List of connections between components. Each connection should follow this schema:
            {
                "from": "component_id",  # ID of the source component
                "to": "component_id",  # ID of the target component
                "label": "optional_label"  # Optional label for the connection
            }
        clusters: List of cluster definitions for grouping components. Each cluster should follow this schema:
            {
                "id": "unique_cluster_id",  # Unique identifier for the cluster
                "label": "cluster_label",  # Display name for the cluster
                "parent": "parent_cluster_id"  # Optional parent cluster ID for nested clusters
            }
            Components can be assigned to clusters using the "cluster" field in the component definition.
            Nested clusters are supported by specifying a "parent" cluster ID.
        output_format: Output format (png, jpg, svg, pdf)
        direction: Diagram direction (TB, BT, LR, RL)

    Returns:
        Dict with success status, file path, and filename
    """
    try:
        # Validate input parameters
        if not components:
            return {
                "success": False,
                "error": "Components list cannot be empty",
                "message": "At least one component is required to generate a diagram"
            }

        # Validate all components are available
        validation_result = validate_components(components)
        if not validation_result["valid"]:
            return {
                "success": False,
                "error": "Component validation failed",
                "message": validation_result["error"],
                "details": validation_result.get("invalid_components", []),
                "validation_info": {
                    "total_components": validation_result.get("total_components", 0),
                    "valid_components": validation_result.get("valid_components", 0),
                    "invalid_components": len(validation_result.get("invalid_components", []))
                }
            }

        logger.info(
            f"Component validation passed: {validation_result['message']}")

        file_path, filename = generate_unique_filename(title, output_format)
        diagram_path_base = file_path.replace(f".{output_format}", "")

        with Diagram(title, filename=diagram_path_base, show=False, direction=direction, outformat=output_format):
            component_instances = {}
            cluster_instances = {}

            # Create cluster instances if clusters are defined
            if clusters:
                # Build cluster hierarchy (parent -> children mapping)
                cluster_hierarchy = {}
                cluster_definitions = {
                    cluster["id"]: cluster for cluster in clusters}

                for cluster in clusters:
                    cluster_id = cluster["id"]
                    parent_id = cluster.get("parent")

                    if parent_id:
                        if parent_id not in cluster_hierarchy:
                            cluster_hierarchy[parent_id] = []
                        cluster_hierarchy[parent_id].append(cluster_id)
                    else:
                        # Root level cluster
                        if "root" not in cluster_hierarchy:
                            cluster_hierarchy["root"] = []
                        cluster_hierarchy["root"].append(cluster_id)

                # Create nested cluster structure
                def create_cluster_context(cluster_id, cluster_definitions, cluster_hierarchy, parent_context=None):
                    """Recursively create nested cluster contexts"""
                    cluster_def = cluster_definitions[cluster_id]
                    cluster_label = cluster_def.get("label", cluster_id)

                    # Create cluster context
                    cluster_context = Cluster(cluster_label)
                    cluster_instances[cluster_id] = {
                        "context": cluster_context,
                        "components": []
                    }

                    # Create child clusters within this cluster
                    child_clusters = cluster_hierarchy.get(cluster_id, [])
                    for child_id in child_clusters:
                        create_cluster_context(
                            child_id, cluster_definitions, cluster_hierarchy, cluster_context)

                    return cluster_context

                # Create all root-level clusters
                root_clusters = cluster_hierarchy.get("root", [])
                for cluster_id in root_clusters:
                    create_cluster_context(
                        cluster_id, cluster_definitions, cluster_hierarchy)

            # Group components by cluster
            clustered_components = {}
            unclustered_components = []

            for comp in components:
                cluster_id = comp.get("cluster")
                if cluster_id and clusters:
                    if cluster_id not in clustered_components:
                        clustered_components[cluster_id] = []
                    clustered_components[cluster_id].append(comp)
                else:
                    unclustered_components.append(comp)

            # Create components within their respective clusters
            def create_component(comp, cluster_context=None):
                comp_id = comp["id"]
                comp_type = comp["type"]
                comp_label = comp.get("label", comp_id)

                parts = comp_type.split(".")
                if len(parts) >= 3:
                    provider, category, component = parts[0], parts[1], parts[2]
                    ComponentClass = get_component_class(
                        provider, category, component)

                    if ComponentClass:
                        if cluster_context:
                            with cluster_context:
                                component_instances[comp_id] = ComponentClass(
                                    comp_label)
                        else:
                            component_instances[comp_id] = ComponentClass(
                                comp_label)
                    else:
                        logger.warning(
                            f"Component class not found for validated component: {comp_type}")

            # Create clustered components
            if clusters:
                for cluster_id, components_in_cluster in clustered_components.items():
                    if cluster_id in cluster_instances:
                        cluster_context = cluster_instances[cluster_id]["context"]
                        for comp in components_in_cluster:
                            create_component(comp, cluster_context)
                            cluster_instances[cluster_id]["components"].append(
                                comp["id"])

            # Create unclustered components
            for comp in unclustered_components:
                create_component(comp)

            # Create connections
            if connections:
                for conn in connections:
                    from_id = conn["from"]
                    to_id = conn["to"]
                    label = conn.get("label", "")

                    if from_id in component_instances and to_id in component_instances:
                        if label:
                            component_instances[from_id] >> Edge(
                                label=label) >> component_instances[to_id]
                        else:
                            component_instances[from_id] >> component_instances[to_id]
                    else:
                        # Log missing component instances in connections
                        missing_components = []
                        if from_id not in component_instances:
                            missing_components.append(from_id)
                        if to_id not in component_instances:
                            missing_components.append(to_id)
                        logger.warning(
                            f"Connection skipped - missing component instances: {missing_components}")

        if os.path.exists(file_path):
            return {
                "success": True,
                "title": title,
                "format": output_format,
                "components_count": len(components),
                "connections_count": len(connections) if connections else 0,
                "clusters_count": len(clusters) if clusters else 0,
                "file_path": file_path,
                "filename": filename,
                "message": f"Diagram '{title}' generated successfully and saved to {filename}",
                "validation_info": {
                    "total_components": validation_result["total_components"],
                    "all_components_valid": True
                }
            }
        else:
            return {
                "success": False,
                "error": "Diagram file was not created",
                "message": "Failed to generate diagram"
            }

    except Exception as e:
        logger.error(f"Error generating diagram: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate diagram due to an error"
        }

# Register the dynamic diagram generation tool
mcp.tool()(generate_dynamic_diagram)

if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
