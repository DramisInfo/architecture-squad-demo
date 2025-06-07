#!/usr/bin/env python3
"""
Architecture Diagram Generator MCP Server

This MCP server provides tools for generating architecture diagrams using the diagrams library.
It supports AWS, Azure, GCP, Kubernetes, and On-Premises components.
"""

import os
import tempfile
import json
import base64
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

try:
    from fastmcp import FastMCP
    from diagrams import Diagram, Cluster, Edge

    # Cloud providers
    from diagrams.aws.compute import EC2, ECS, EKS, Lambda
    from diagrams.aws.database import RDS, Dynamodb, ElastiCache, Redshift
    from diagrams.aws.network import ELB, Route53, VPC, InternetGateway
    from diagrams.aws.storage import S3
    from diagrams.aws.integration import SQS, SNS

    from diagrams.azure.compute import VM, ContainerInstances, AKS, FunctionApps
    from diagrams.azure.database import SQLDatabases, CosmosDb, CacheForRedis
    from diagrams.azure.network import LoadBalancers, ApplicationGateway, VirtualNetworks
    from diagrams.azure.storage import StorageAccounts, BlobStorage
    from diagrams.azure.integration import ServiceBus, EventGridTopics

    from diagrams.gcp.compute import ComputeEngine, GKE, Functions as GCPFunctions
    from diagrams.gcp.database import SQL, Firestore
    from diagrams.gcp.network import LoadBalancing, DNS
    from diagrams.gcp.storage import GCS
    from diagrams.gcp.analytics import PubSub, Dataflow, BigQuery

    from diagrams.k8s.compute import Pod, Deployment, StatefulSet, ReplicaSet
    from diagrams.k8s.network import Service, Ingress
    from diagrams.k8s.storage import PV, PVC
    from diagrams.k8s.clusterconfig import HPA

    from diagrams.onprem.compute import Server
    from diagrams.onprem.database import PostgreSQL, MySQL, MongoDB
    from diagrams.onprem.network import Nginx, Apache
    from diagrams.onprem.inmemory import Redis
    from diagrams.onprem.queue import Kafka, RabbitMQ
    from diagrams.onprem.monitoring import Prometheus, Grafana

except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Please install the required dependencies:")
    print("pip install fastmcp diagrams python-dotenv pillow")
    exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("Diagram Generator Server")

# Component mappings for easy lookup
COMPONENT_MAPPINGS = {
    "aws": {
        "compute": {
            "ec2": EC2,
            "ecs": ECS,
            "eks": EKS,
            "lambda": Lambda
        },
        "database": {
            "rds": RDS,
            "dynamodb": Dynamodb,
            "elasticache": ElastiCache,
            "redshift": Redshift
        },
        "network": {
            "elb": ELB,
            "route53": Route53,
            "vpc": VPC,
            "igw": InternetGateway
        },
        "storage": {
            "s3": S3
        },
        "integration": {
            "sqs": SQS,
            "sns": SNS
        }
    },
    "azure": {
        "compute": {
            "vm": VM,
            "aci": ContainerInstances,
            "aks": AKS,
            "functions": FunctionApps
        },
        "database": {
            "sql": SQLDatabases,
            "cosmosdb": CosmosDb,
            "redis": CacheForRedis
        },
        "network": {
            "lb": LoadBalancers,
            "appgw": ApplicationGateway,
            "vnet": VirtualNetworks
        },
        "storage": {
            "storage": StorageAccounts,
            "blob": BlobStorage
        },
        "integration": {
            "servicebus": ServiceBus,
            "eventgrid": EventGridTopics
        }
    },
    "gcp": {
        "compute": {
            "gce": ComputeEngine,
            "gke": GKE,
            "functions": GCPFunctions
        },
        "database": {
            "sql": SQL,
            "bigquery": BigQuery,
            "firestore": Firestore
        },
        "network": {
            "lb": LoadBalancing,
            "dns": DNS
        },
        "storage": {
            "gcs": GCS
        },
        "analytics": {
            "pubsub": PubSub,
            "dataflow": Dataflow
        }
    },
    "k8s": {
        "compute": {
            "pod": Pod,
            "deployment": Deployment,
            "statefulset": StatefulSet,
            "replicaset": ReplicaSet
        },
        "network": {
            "service": Service,
            "ingress": Ingress
        },
        "storage": {
            "pv": PV,
            "pvc": PVC
        },
        "config": {
            "hpa": HPA
        }
    },
    "onprem": {
        "compute": {
            "server": Server
        },
        "database": {
            "postgresql": PostgreSQL,
            "mysql": MySQL,
            "mongodb": MongoDB
        },
        "network": {
            "nginx": Nginx,
            "apache": Apache
        },
        "memory": {
            "redis": Redis
        },
        "queue": {
            "kafka": Kafka,
            "rabbitmq": RabbitMQ
        },
        "monitoring": {
            "prometheus": Prometheus,
            "grafana": Grafana
        }
    }
}


def get_component_class(provider: str, category: str, component: str):
    """Get the diagrams component class for a given provider/category/component"""
    try:
        return COMPONENT_MAPPINGS[provider.lower()][category.lower()][component.lower()]
    except KeyError:
        logger.warning(
            f"Component not found: {provider}/{category}/{component}")
        return None


@mcp.tool()
async def generate_simple_diagram(
    title: str,
    components: List[Dict[str, Any]],
    connections: List[Dict[str, Any]] = None,
    output_format: str = "png",
    direction: str = "TB",
    show_labels: bool = True
) -> Dict[str, Any]:
    """
    Generate a simple architecture diagram with components and connections.

    Args:
        title: The title of the diagram
        components: List of components with format:
            [{"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"}]
        connections: List of connections with format:
            [{"from": "web1", "to": "db1", "label": "queries"}]
        output_format: Output format (png, jpg, svg, pdf)
        direction: Diagram direction (TB, BT, LR, RL)
        show_labels: Whether to show component labels

    Returns:
        Dict with success status, file path, and base64 encoded image
    """
    try:
        # Create a temporary directory for the diagram
        with tempfile.TemporaryDirectory() as temp_dir:
            diagram_path = os.path.join(temp_dir, f"diagram.{output_format}")

            # Create the diagram
            with Diagram(title, filename=diagram_path.replace(f".{output_format}", ""),
                         show=False, direction=direction, outformat=output_format):

                # Create component instances
                component_instances = {}

                for comp in components:
                    comp_id = comp["id"]
                    comp_type = comp["type"]
                    comp_label = comp.get("label", comp_id)

                    # Parse component type (e.g., "aws.compute.ec2")
                    parts = comp_type.split(".")
                    if len(parts) >= 3:
                        provider, category, component = parts[0], parts[1], parts[2]
                        ComponentClass = get_component_class(
                            provider, category, component)

                        if ComponentClass:
                            component_instances[comp_id] = ComponentClass(
                                comp_label)
                        else:
                            logger.warning(
                                f"Unknown component type: {comp_type}")
                            continue
                    else:
                        logger.warning(
                            f"Invalid component type format: {comp_type}")
                        continue

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

            # Read the generated image and encode as base64
            if os.path.exists(diagram_path):
                with open(diagram_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()

                return {
                    "success": True,
                    "title": title,
                    "format": output_format,
                    "components_count": len(components),
                    "connections_count": len(connections) if connections else 0,
                    "image_base64": image_data,
                    "message": f"Diagram '{title}' generated successfully"
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


@mcp.tool()
async def generate_clustered_diagram(
    title: str,
    clusters: List[Dict[str, Any]],
    connections: List[Dict[str, Any]] = None,
    output_format: str = "png",
    direction: str = "TB"
) -> Dict[str, Any]:
    """
    Generate a clustered architecture diagram with grouped components.

    Args:
        title: The title of the diagram
        clusters: List of clusters with format:
            [{"name": "Web Tier", "components": [{"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"}]}]
        connections: List of connections between components
        output_format: Output format (png, jpg, svg, pdf)
        direction: Diagram direction (TB, BT, LR, RL)

    Returns:
        Dict with success status, file path, and base64 encoded image
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            diagram_path = os.path.join(temp_dir, f"diagram.{output_format}")

            with Diagram(title, filename=diagram_path.replace(f".{output_format}", ""),
                         show=False, direction=direction, outformat=output_format):

                component_instances = {}

                # Create clusters with components
                for cluster_def in clusters:
                    cluster_name = cluster_def["name"]
                    cluster_components = cluster_def["components"]

                    with Cluster(cluster_name):
                        for comp in cluster_components:
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

            # Read and encode the image
            if os.path.exists(diagram_path):
                with open(diagram_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()

                return {
                    "success": True,
                    "title": title,
                    "format": output_format,
                    "clusters_count": len(clusters),
                    "connections_count": len(connections) if connections else 0,
                    "image_base64": image_data,
                    "message": f"Clustered diagram '{title}' generated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Diagram file was not created"
                }

    except Exception as e:
        logger.error(f"Error generating clustered diagram: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
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
        Dict with success status and base64 encoded image
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            diagram_path = os.path.join(temp_dir, "aws_web_app.png")

            with Diagram(title, filename=diagram_path.replace(".png", ""), show=False):
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

            # Read and encode the image
            if os.path.exists(diagram_path):
                with open(diagram_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()

                return {
                    "success": True,
                    "title": title,
                    "format": "png",
                    "template": "aws_web_app",
                    "image_base64": image_data,
                    "message": f"AWS web application diagram generated successfully"
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


@mcp.tool()
async def generate_kubernetes_diagram(
    title: str = "Kubernetes Architecture",
    replicas: int = 3,
    include_ingress: bool = True,
    include_hpa: bool = True,
    include_storage: bool = False
) -> Dict[str, Any]:
    """
    Generate a predefined Kubernetes architecture diagram.

    Args:
        title: The title of the diagram
        replicas: Number of pod replicas
        include_ingress: Include Ingress controller
        include_hpa: Include Horizontal Pod Autoscaler
        include_storage: Include persistent storage

    Returns:
        Dict with success status and base64 encoded image
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            diagram_path = os.path.join(temp_dir, "k8s_arch.png")

            with Diagram(title, filename=diagram_path.replace(".png", ""), show=False):
                # Ingress
                if include_ingress:
                    ingress = Ingress("ingress")

                # Service
                svc = Service("service")

                # Pods
                pods = []
                for i in range(replicas):
                    pods.append(Pod(f"pod{i+1}"))

                # Deployment and ReplicaSet
                rs = ReplicaSet("replicaset")
                deployment = Deployment("deployment")

                # HPA
                if include_hpa:
                    hpa = HPA("hpa")

                # Storage
                if include_storage:
                    pvc = PVC("pvc")
                    pv = PV("pv")

                # Create connections
                if include_ingress:
                    ingress >> svc

                # Connect service to all pods
                for pod in pods:
                    svc >> pod

                # Connect replicaset to all pods and deployment to replicaset
                for pod in pods:
                    rs >> pod
                deployment >> rs

                if include_hpa:
                    hpa >> deployment

                if include_storage:
                    for pod in pods:
                        pod >> pvc
                    pv >> pvc

            # Read and encode the image
            if os.path.exists(diagram_path):
                with open(diagram_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()

                return {
                    "success": True,
                    "title": title,
                    "format": "png",
                    "template": "kubernetes",
                    "replicas": replicas,
                    "image_base64": image_data,
                    "message": f"Kubernetes architecture diagram generated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Diagram file was not created"
                }

    except Exception as e:
        logger.error(f"Error generating Kubernetes diagram: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def list_available_components() -> Dict[str, Any]:
    """
    List all available components that can be used in diagrams.

    Returns:
        Dict with all available providers, categories, and components
    """
    try:
        return {
            "success": True,
            "components": COMPONENT_MAPPINGS,
            "providers": list(COMPONENT_MAPPINGS.keys()),
            "message": "Available components listed successfully"
        }
    except Exception as e:
        logger.error(f"Error listing components: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
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
        Dict with success status and base64 encoded image
    """
    try:
        if services is None:
            services = ["User Service", "Order Service",
                        "Payment Service", "Inventory Service"]

        with tempfile.TemporaryDirectory() as temp_dir:
            diagram_path = os.path.join(temp_dir, "microservices.png")

            with Diagram(title, filename=diagram_path.replace(".png", ""), show=False):
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

            # Read and encode the image
            if os.path.exists(diagram_path):
                with open(diagram_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()

                return {
                    "success": True,
                    "title": title,
                    "format": "png",
                    "template": "microservices",
                    "provider": provider,
                    "services_count": len(services),
                    "image_base64": image_data,
                    "message": f"Microservices architecture diagram generated successfully"
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

if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
