#!/usr/bin/env python3
"""
Utility functions for the Diagram Generator MCP Server
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from .config import COMPONENT_MAPPINGS, VOLUME_MOUNT_PATH, logger


def generate_unique_filename(title: str, output_format: str = "png") -> tuple[str, str]:
    """
    Generate a unique filename for a diagram.

    Args:
        title: The title of the diagram
        output_format: The output format (png, jpg, svg, pdf)

    Returns:
        Tuple of (full_file_path, filename_only)
    """
    # Create a safe filename from the title
    safe_title = "".join(c for c in title if c.isalnum()
                         or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')

    # Generate unique identifier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]

    # Create filename
    filename = f"{safe_title}_{timestamp}_{unique_id}.{output_format}"
    full_path = os.path.join(VOLUME_MOUNT_PATH, filename)

    return full_path, filename


def get_component_class(provider: str, category: str, component: str):
    """Get the diagrams component class for a given provider/category/component"""
    try:
        return COMPONENT_MAPPINGS[provider.lower()][category.lower()][component.lower()]
    except KeyError:
        logger.warning(
            f"Component not found: {provider}/{category}/{component}")
        return None


def list_available_components() -> Dict[str, Any]:
    """
    List all available components that can be used in diagrams.

    Returns:
        Dict with all available providers, categories, and components
    """
    try:
        available_components = {}
        for provider, categories in COMPONENT_MAPPINGS.items():
            available_components[provider] = {}
            for category, components in categories.items():
                available_components[provider][category] = list(
                    components.keys())

        return {
            "success": True,
            "providers": list(COMPONENT_MAPPINGS.keys()),
            "components": available_components,
            "total_providers": len(COMPONENT_MAPPINGS),
            "message": "Successfully retrieved all available components"
        }
    except Exception as e:
        logger.error(f"Error listing components: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
