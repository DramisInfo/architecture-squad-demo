#!/usr/bin/env python3
"""
Main MCP Server for Architecture Diagram Generator

This MCP server provides tools for generating architecture diagrams using the diagrams library.
It supports AWS, Azure, GCP, Kubernetes, and On-Premises components.
"""

from fastmcp import FastMCP
from core.config import logger

# Import all diagram generation functions
from diagram_generators.simple_diagram import generate_simple_diagram
from diagram_generators.clustered_diagram import generate_clustered_diagram
from diagram_generators.aws_diagrams import generate_aws_web_app_diagram
from diagram_generators.kubernetes_diagrams import generate_kubernetes_diagram
from diagram_generators.microservices_diagrams import generate_microservices_diagram
from core.utils import list_available_components

# Create MCP server
mcp = FastMCP("Diagram Generator Server")

# Register all tools with the MCP server
mcp.tool()(generate_simple_diagram)
mcp.tool()(generate_clustered_diagram)
mcp.tool()(generate_aws_web_app_diagram)
mcp.tool()(generate_kubernetes_diagram)
mcp.tool()(generate_microservices_diagram)
mcp.tool()(list_available_components)

if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
