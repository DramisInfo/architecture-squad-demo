#!/usr/bin/env python3
"""
Test script for cluster support in the diagram generator MCP server
"""

import asyncio
import json
from server import generate_dynamic_diagram, list_available_components


async def test_basic_cluster_support():
    """Test basic cluster functionality with simple grouping"""
    print("🧪 Testing basic cluster support...")

    # Define components with cluster assignments
    components = [
        {
            "id": "user",
            "type": "aws.compute.EC2",
            "label": "User"
        },
        {
            "id": "lb",
            "type": "aws.network.ELB",
            "label": "Load Balancer"
        },
        {
            "id": "web1",
            "type": "aws.compute.ECS",
            "label": "Web Server 1",
            "cluster": "web_cluster"
        },
        {
            "id": "web2",
            "type": "aws.compute.ECS",
            "label": "Web Server 2",
            "cluster": "web_cluster"
        },
        {
            "id": "db_primary",
            "type": "aws.database.RDS",
            "label": "Primary DB",
            "cluster": "db_cluster"
        },
        {
            "id": "db_replica",
            "type": "aws.database.RDS",
            "label": "Replica DB",
            "cluster": "db_cluster"
        }
    ]

    # Define clusters
    clusters = [
        {
            "id": "web_cluster",
            "label": "Web Servers"
        },
        {
            "id": "db_cluster",
            "label": "Database Cluster"
        }
    ]

    # Define connections
    connections = [
        {"from": "user", "to": "lb"},
        {"from": "lb", "to": "web1"},
        {"from": "lb", "to": "web2"},
        {"from": "web1", "to": "db_primary"},
        {"from": "web2", "to": "db_primary"},
        {"from": "db_primary", "to": "db_replica", "label": "replication"}
    ]

    result = await generate_dynamic_diagram(
        title="Basic Cluster Test",
        components=components,
        connections=connections,
        clusters=clusters
    )

    if result["success"]:
        print(f"✅ Basic cluster test passed - {result['message']}")
        print(
            f"   📊 Components: {result['components_count']}, Clusters: {result['clusters_count']}")
        return True
    else:
        print(
            f"❌ Basic cluster test failed - {result.get('error', 'Unknown error')}")
        return False


async def test_nested_cluster_support():
    """Test nested cluster functionality"""
    print("🧪 Testing nested cluster support...")

    # Define components with nested cluster assignments
    components = [
        {
            "id": "source",
            "type": "k8s.compute.Pod",
            "label": "Source System"
        },
        {
            "id": "worker1",
            "type": "aws.compute.ECS",
            "label": "Worker 1",
            "cluster": "event_workers"
        },
        {
            "id": "worker2",
            "type": "aws.compute.ECS",
            "label": "Worker 2",
            "cluster": "event_workers"
        },
        {
            "id": "queue",
            "type": "aws.integration.SQS",
            "label": "Event Queue",
            "cluster": "event_flows"
        },
        {
            "id": "proc1",
            "type": "aws.compute.Lambda",
            "label": "Processor 1",
            "cluster": "processing"
        },
        {
            "id": "proc2",
            "type": "aws.compute.Lambda",
            "label": "Processor 2",
            "cluster": "processing"
        },
        {
            "id": "storage",
            "type": "aws.storage.S3",
            "label": "Event Store"
        }
    ]

    # Define nested clusters
    clusters = [
        {
            "id": "event_flows",
            "label": "Event Flows"
        },
        {
            "id": "event_workers",
            "label": "Event Workers",
            "parent": "event_flows"
        },
        {
            "id": "processing",
            "label": "Processing",
            "parent": "event_flows"
        }
    ]

    # Define connections
    connections = [
        {"from": "source", "to": "worker1"},
        {"from": "source", "to": "worker2"},
        {"from": "worker1", "to": "queue"},
        {"from": "worker2", "to": "queue"},
        {"from": "queue", "to": "proc1"},
        {"from": "queue", "to": "proc2"},
        {"from": "proc1", "to": "storage"},
        {"from": "proc2", "to": "storage"}
    ]

    result = await generate_dynamic_diagram(
        title="Nested Cluster Test",
        components=components,
        connections=connections,
        clusters=clusters
    )

    if result["success"]:
        print(f"✅ Nested cluster test passed - {result['message']}")
        print(
            f"   📊 Components: {result['components_count']}, Clusters: {result['clusters_count']}")
        return True
    else:
        print(
            f"❌ Nested cluster test failed - {result.get('error', 'Unknown error')}")
        return False


async def test_mixed_cluster_and_standalone():
    """Test mixed scenario with both clustered and standalone components"""
    print("🧪 Testing mixed cluster and standalone components...")

    components = [
        {
            "id": "dns",
            "type": "aws.network.Route53",
            "label": "DNS"
        },
        {
            "id": "cdn",
            "type": "aws.network.CloudFront",
            "label": "CDN"
        },
        {
            "id": "api1",
            "type": "aws.compute.Lambda",
            "label": "API Gateway 1",
            "cluster": "api_cluster"
        },
        {
            "id": "api2",
            "type": "aws.compute.Lambda",
            "label": "API Gateway 2",
            "cluster": "api_cluster"
        },
        {
            "id": "cache",
            "type": "aws.database.ElastiCache",
            "label": "Redis Cache"
        }
    ]

    clusters = [
        {
            "id": "api_cluster",
            "label": "API Services"
        }
    ]

    connections = [
        {"from": "dns", "to": "cdn"},
        {"from": "cdn", "to": "api1"},
        {"from": "cdn", "to": "api2"},
        {"from": "api1", "to": "cache"},
        {"from": "api2", "to": "cache"}
    ]

    result = await generate_dynamic_diagram(
        title="Mixed Cluster Test",
        components=components,
        connections=connections,
        clusters=clusters
    )

    if result["success"]:
        print(f"✅ Mixed cluster test passed - {result['message']}")
        print(
            f"   📊 Components: {result['components_count']}, Clusters: {result['clusters_count']}")
        return True
    else:
        print(
            f"❌ Mixed cluster test failed - {result.get('error', 'Unknown error')}")
        return False


async def test_no_clusters():
    """Test that existing functionality still works without clusters"""
    print("🧪 Testing backward compatibility (no clusters)...")

    components = [
        {
            "id": "web",
            "type": "aws.compute.EC2",
            "label": "Web Server"
        },
        {
            "id": "db",
            "type": "aws.database.RDS",
            "label": "Database"
        }
    ]

    connections = [
        {"from": "web", "to": "db"}
    ]

    # No clusters parameter
    result = await generate_dynamic_diagram(
        title="No Clusters Test",
        components=components,
        connections=connections
    )

    if result["success"]:
        print(f"✅ Backward compatibility test passed - {result['message']}")
        print(
            f"   📊 Components: {result['components_count']}, Clusters: {result['clusters_count']}")
        return True
    else:
        print(
            f"❌ Backward compatibility test failed - {result.get('error', 'Unknown error')}")
        return False


async def print_usage_examples():
    """Print usage examples for documentation"""
    print("\n📚 CLUSTER USAGE EXAMPLES FOR MCP AGENTS:")
    print("=" * 60)

    print("\n1. BASIC CLUSTERING:")
    print("   Group related components together using clusters")

    basic_example = {
        "components": [
            {"id": "web1", "type": "aws.compute.ECS",
                "label": "Web 1", "cluster": "web_tier"},
            {"id": "web2", "type": "aws.compute.ECS",
                "label": "Web 2", "cluster": "web_tier"},
            {"id": "db1", "type": "aws.database.RDS",
                "label": "DB Primary", "cluster": "db_tier"},
            {"id": "db2", "type": "aws.database.RDS",
                "label": "DB Replica", "cluster": "db_tier"}
        ],
        "clusters": [
            {"id": "web_tier", "label": "Web Tier"},
            {"id": "db_tier", "label": "Database Tier"}
        ],
        "connections": [
            {"from": "web1", "to": "db1"},
            {"from": "web2", "to": "db1"},
            {"from": "db1", "to": "db2", "label": "replication"}
        ]
    }

    print(json.dumps(basic_example, indent=2))

    print("\n2. NESTED CLUSTERING:")
    print("   Create hierarchical groupings with parent-child relationships")

    nested_example = {
        "components": [
            {"id": "worker1", "type": "aws.compute.ECS",
                "label": "Worker 1", "cluster": "workers"},
            {"id": "worker2", "type": "aws.compute.ECS",
                "label": "Worker 2", "cluster": "workers"},
            {"id": "proc1", "type": "aws.compute.Lambda",
                "label": "Processor 1", "cluster": "processors"}
        ],
        "clusters": [
            {"id": "event_system", "label": "Event Processing System"},
            {"id": "workers", "label": "Workers", "parent": "event_system"},
            {"id": "processors", "label": "Processors", "parent": "event_system"}
        ]
    }

    print(json.dumps(nested_example, indent=2))

    print("\n3. MIXED CLUSTERING:")
    print("   Combine clustered and standalone components")

    mixed_example = {
        "components": [
            {"id": "dns", "type": "aws.network.Route53",
                "label": "DNS"},  # standalone
            {"id": "api1", "type": "aws.compute.Lambda",
                "label": "API 1", "cluster": "apis"},
            {"id": "api2", "type": "aws.compute.Lambda",
                "label": "API 2", "cluster": "apis"},
            {"id": "cache", "type": "aws.database.ElastiCache",
                "label": "Cache"}  # standalone
        ],
        "clusters": [
            {"id": "apis", "label": "API Services"}
        ]
    }

    print(json.dumps(mixed_example, indent=2))

    print("\n4. CLUSTER FIELD REFERENCE:")
    print("   - Component 'cluster' field: ID of cluster to assign component to")
    print("   - Cluster 'parent' field: ID of parent cluster for nesting")
    print("   - Components without 'cluster' field remain standalone")
    print("   - Unlimited nesting depth supported")

    print("\n" + "=" * 60)


async def main():
    """Run all cluster tests"""
    print("🚀 Testing Cluster Support in Diagram Generator MCP Server")
    print("=" * 60)

    tests = [
        test_no_clusters,
        test_basic_cluster_support,
        test_nested_cluster_support,
        test_mixed_cluster_and_standalone
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if await test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
            print()

    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All cluster tests passed! The feature is ready to use.")
        await print_usage_examples()
    else:
        print("⚠️  Some tests failed. Please review the implementation.")


if __name__ == "__main__":
    asyncio.run(main())
