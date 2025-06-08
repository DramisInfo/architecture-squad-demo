#!/usr/bin/env python3
"""
Configuration and shared constants for the Diagram Generator MCP Server
"""

import os
import logging
from pathlib import Path

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

# Volume mount path where diagrams will be saved
VOLUME_MOUNT_PATH = "/tmp"

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
