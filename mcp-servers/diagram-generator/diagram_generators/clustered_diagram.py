#!/usr/bin/env python3
"""
Diagram generation functions for the Diagram Generator MCP Server
"""

import os
from typing import Dict, Any, List

from core.config import Diagram, Edge, logger
from core.utils import generate_unique_filename, get_component_class


async def generate_diagram(
    title: str,
    components: List[Dict[str, Any]],
    connections: List[Dict[str, Any]] = None,
    output_format: str = "png",
    direction: str = "TB"
) -> Dict[str, Any]:
    """
    Generate an architecture diagram with components.

    Args:
        title: The title of the diagram
        components: List of components with format:
            [{"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"}]
        connections: List of connections between components
        output_format: Output format (png, jpg, svg, pdf)
        direction: Diagram direction (TB, BT, LR, RL)

    Returns:
        Dict with success status, file path, and filename
    """
    try:
        # Generate unique filename for the volume mount
        file_path, filename = generate_unique_filename(title, output_format)

        # Create the diagram directly to the volume mount path
        diagram_path_base = file_path.replace(f".{output_format}", "")

        with Diagram(title, filename=diagram_path_base,
                     show=False, direction=direction, outformat=output_format):

            component_instances = {}

            # Create components
            for comp in components:
                comp_id = comp["id"]
                comp_type = comp["type"]
                comp_label = comp.get("label", comp_id)

                # Parse component type
                parts = comp_type.split(".")
                if len(parts) >= 3:
                    provider, category, component = parts[0], parts[1], parts[2]
                    ComponentClass = get_component_class(
                        provider, category, component)

                    if ComponentClass:
                        component_instances[comp_id] = ComponentClass(
                            comp_label)

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

        # Check if the diagram file was created
        if os.path.exists(file_path):
            return {
                "success": True,
                "title": title,
                "format": output_format,
                "components_count": len(components),
                "connections_count": len(connections) if connections else 0,
                "file_path": file_path,
                "filename": filename,
                "message": f"Diagram '{title}' generated successfully and saved to {filename}"
            }
        else:
            return {
                "success": False,
                "error": "Diagram file was not created"
            }

    except Exception as e:
        logger.error(f"Error generating diagram: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
