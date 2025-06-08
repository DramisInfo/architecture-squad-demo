#!/usr/bin/env python3
"""
Kubernetes-specific diagram generation functions for the Diagram Generator MCP Server
"""

import os
from typing import Dict, Any

from core.config import (
    Diagram, Cluster, Pod, Service, Ingress, ReplicaSet, Deployment, HPA, PVC, PV, logger
)
from core.utils import generate_unique_filename


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
        Dict with success status, file path, and filename
    """
    try:
        # Generate unique filename for the volume mount
        file_path, filename = generate_unique_filename(title, "png")

        # Create the diagram directly to the volume mount path
        diagram_path_base = file_path.replace(".png", "")

        with Diagram(title, filename=diagram_path_base, show=False):
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

        # Check if the diagram file was created
        if os.path.exists(file_path):
            return {
                "success": True,
                "title": title,
                "format": "png",
                "template": "kubernetes",
                "replicas": replicas,
                "file_path": file_path,
                "filename": filename,
                "message": f"Kubernetes architecture diagram generated successfully and saved to {filename}"
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
