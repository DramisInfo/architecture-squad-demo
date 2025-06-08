#!/usr/bin/env python3
"""
AWS-specific diagram generation functions for the Diagram Generator MCP Server
"""

import os
from typing import Dict, Any

from core.config import (
    Diagram, Cluster, Route53, ELB, EC2, ECS, RDS, S3, ElastiCache, logger
)
from core.utils import generate_unique_filename


async def generate_aws_web_app_diagram(
    title: str = "AWS Web Application",
    include_cdn: bool = True,
    include_cache: bool = True,
    include_monitoring: bool = False,
    multi_az: bool = True
) -> Dict[str, Any]:
    """
    Generate a predefined AWS web application architecture diagram.

    Args:
        title: The title of the diagram
        include_cdn: Include CloudFront CDN
        include_cache: Include ElastiCache
        include_monitoring: Include CloudWatch monitoring
        multi_az: Use multi-AZ deployment

    Returns:
        Dict with success status, file path, and filename
    """
    try:
        # Generate unique filename for the volume mount
        file_path, filename = generate_unique_filename(title, "png")

        # Create the diagram directly to the volume mount path
        diagram_path_base = file_path.replace(".png", "")

        with Diagram(title, filename=diagram_path_base, show=False):
            # DNS and Load Balancer
            dns = Route53("DNS")
            lb = ELB("Load Balancer")

            # Web Servers
            with Cluster("Web Tier"):
                web_servers = [EC2("Web1"), EC2("Web2")]
                if multi_az:
                    web_servers.append(EC2("Web3"))

            # Application Servers
            with Cluster("Application Tier"):
                app_servers = [ECS("App1"), ECS("App2")]

            # Database
            with Cluster("Database Tier"):
                db_primary = RDS("Primary DB")
                if multi_az:
                    db_replica = RDS("Replica DB")
                    db_primary - db_replica

            # Storage
            storage = S3("Static Assets")

            # Optional components
            cache = None
            if include_cache:
                cache = ElastiCache("Cache")

            # Create connections
            dns >> lb

            # Connect load balancer to web servers
            for web_server in web_servers:
                lb >> web_server

            # Connect web servers to app servers
            for web_server in web_servers:
                for app_server in app_servers:
                    web_server >> app_server

            # Connect app servers to database
            for app_server in app_servers:
                app_server >> db_primary

            if cache:
                for app_server in app_servers:
                    app_server >> cache

            # Connect web servers to storage
            for web_server in web_servers:
                web_server >> storage

        # Check if the diagram file was created
        if os.path.exists(file_path):
            return {
                "success": True,
                "title": title,
                "format": "png",
                "template": "aws_web_app",
                "file_path": file_path,
                "filename": filename,
                "message": f"AWS web application diagram generated successfully and saved to {filename}"
            }
        else:
            return {
                "success": False,
                "error": "Diagram file was not created"
            }

    except Exception as e:
        logger.error(f"Error generating AWS web app diagram: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
