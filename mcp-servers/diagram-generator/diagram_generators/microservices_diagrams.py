#!/usr/bin/env python3
"""
Microservices diagram generation functions for the Diagram Generator MCP Server
"""

import os
from typing import Dict, Any, List

from core.config import (
    Diagram, Cluster, ELB, ApplicationGateway, LoadBalancing,
    ECS, ContainerInstances, GKE, RDS, SQLDatabases, CosmosDb, SQL, Firestore,
    ElastiCache, CacheForRedis, SQS, ServiceBus, PubSub, logger
)
from core.utils import generate_unique_filename


async def generate_microservices_diagram(
    title: str = "Microservices Architecture",
    provider: str = "aws",
    services: List[str] = None,
    include_gateway: bool = True,
    include_database: bool = True,
    include_cache: bool = True,
    include_queue: bool = True
) -> Dict[str, Any]:
    """
    Generate a microservices architecture diagram.

    Args:
        title: The title of the diagram
        provider: Cloud provider (aws, azure, gcp)
        services: List of microservice names
        include_gateway: Include API Gateway
        include_database: Include databases
        include_cache: Include caching layer
        include_queue: Include message queue

    Returns:
        Dict with success status, file path, and filename
    """
    try:
        if services is None:
            services = ["User Service", "Order Service",
                        "Payment Service", "Inventory Service"]

        # Generate unique filename for the volume mount
        file_path, filename = generate_unique_filename(title, "png")

        # Create the diagram directly to the volume mount path
        diagram_path_base = file_path.replace(".png", "")

        with Diagram(title, filename=diagram_path_base, show=False):
            # API Gateway
            if include_gateway:
                if provider.lower() == "aws":
                    gateway = ELB("API Gateway")
                elif provider.lower() == "azure":
                    gateway = ApplicationGateway("API Gateway")
                else:  # GCP
                    gateway = LoadBalancing("API Gateway")

            # Microservices
            with Cluster("Microservices"):
                service_instances = []
                for service_name in services:
                    if provider.lower() == "aws":
                        service_instances.append(ECS(service_name))
                    elif provider.lower() == "azure":
                        service_instances.append(
                            ContainerInstances(service_name))
                    else:  # GCP
                        service_instances.append(GKE(service_name))

            # Databases
            if include_database:
                with Cluster("Databases"):
                    if provider.lower() == "aws":
                        databases = [RDS("User DB"), RDS(
                            "Order DB"), RDS("Payment DB")]
                    elif provider.lower() == "azure":
                        databases = [SQLDatabases("User DB"), SQLDatabases(
                            "Order DB"), CosmosDb("Payment DB")]
                    else:  # GCP
                        databases = [SQL("User DB"), SQL(
                            "Order DB"), Firestore("Payment DB")]

            # Cache
            if include_cache:
                if provider.lower() == "aws":
                    cache = ElastiCache("Cache")
                elif provider.lower() == "azure":
                    cache = CacheForRedis("Cache")
                else:  # GCP
                    cache = None  # GCP doesn't have a direct equivalent in diagrams

            # Message Queue
            if include_queue:
                if provider.lower() == "aws":
                    queue = SQS("Message Queue")
                elif provider.lower() == "azure":
                    queue = ServiceBus("Message Queue")
                else:  # GCP
                    queue = PubSub("Message Queue")

            # Create connections
            if include_gateway:
                for service in service_instances:
                    gateway >> service

            if include_database:
                for i, service in enumerate(service_instances[:len(databases)]):
                    service >> databases[i]

            if include_cache and cache:
                for service in service_instances:
                    service >> cache

            if include_queue:
                for service in service_instances:
                    service >> queue

        # Check if the diagram file was created
        if os.path.exists(file_path):
            return {
                "success": True,
                "title": title,
                "format": "png",
                "template": "microservices",
                "provider": provider,
                "services_count": len(services),
                "file_path": file_path,
                "filename": filename,
                "message": f"Microservices architecture diagram generated successfully and saved to {filename}"
            }
        else:
            return {
                "success": False,
                "error": "Diagram file was not created"
            }

    except Exception as e:
        logger.error(f"Error generating microservices diagram: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
