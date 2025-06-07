# Architecture Diagram Generator MCP Server

This MCP server provides tools for generating architecture diagrams using the [diagrams](https://diagrams.mingrammer.com/) library. It supports creating visual architecture diagrams for AWS, Azure, GCP, Kubernetes, and On-Premises components.

## Features

- **Simple Diagrams**: Create basic architecture diagrams with components and connections
- **Clustered Diagrams**: Group components into logical clusters (tiers, environments, etc.)
- **Template Diagrams**: Pre-built templates for common architectures:
  - AWS Web Applications
  - Kubernetes Deployments
  - Microservices Architecture
- **Multi-Cloud Support**: Support for AWS, Azure, GCP, Kubernetes, and On-Premises components
- **Flexible Output**: Generate diagrams in PNG, JPG, SVG, or PDF formats
- **Base64 Encoding**: Returns diagrams as base64-encoded strings for easy integration

## Prerequisites

### System Requirements
- Python 3.7 or higher
- Graphviz (required by the diagrams library)

### Install Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install graphviz
```

**macOS (with Homebrew):**
```bash
brew install graphviz
```

**Windows (with Chocolatey):**
```bash
choco install graphviz
```

**Windows (Manual):**
Download and install from: https://graphviz.gitlab.io/download/

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Verify Graphviz installation:
```bash
dot -V
```

## Usage

### Running the MCP Server

```bash
python server.py
```

### Available Tools

#### 1. `generate_simple_diagram`
Create a basic architecture diagram with components and connections.

**Parameters:**
- `title` (str): The title of the diagram
- `components` (List[Dict]): List of components with format:
  ```json
  [{"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"}]
  ```
- `connections` (List[Dict], optional): List of connections with format:
  ```json
  [{"from": "web1", "to": "db1", "label": "queries"}]
  ```
- `output_format` (str, default: "png"): Output format (png, jpg, svg, pdf)
- `direction` (str, default: "TB"): Diagram direction (TB, BT, LR, RL)
- `show_labels` (bool, default: true): Whether to show component labels

#### 2. `generate_clustered_diagram`
Create a diagram with components grouped into clusters.

**Parameters:**
- `title` (str): The title of the diagram
- `clusters` (List[Dict]): List of clusters with format:
  ```json
  [{
    "name": "Web Tier",
    "components": [{"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"}]
  }]
  ```
- `connections` (List[Dict], optional): List of connections between components
- `output_format` (str, default: "png"): Output format
- `direction` (str, default: "TB"): Diagram direction

#### 3. `generate_aws_web_app_diagram`
Generate a predefined AWS web application architecture.

**Parameters:**
- `title` (str, default: "AWS Web Application"): The title of the diagram
- `include_cdn` (bool, default: true): Include CloudFront CDN
- `include_cache` (bool, default: true): Include ElastiCache
- `include_monitoring` (bool, default: false): Include CloudWatch monitoring
- `multi_az` (bool, default: true): Use multi-AZ deployment

#### 4. `generate_kubernetes_diagram`
Generate a predefined Kubernetes architecture diagram.

**Parameters:**
- `title` (str, default: "Kubernetes Architecture"): The title of the diagram
- `replicas` (int, default: 3): Number of pod replicas
- `include_ingress` (bool, default: true): Include Ingress controller
- `include_hpa` (bool, default: true): Include Horizontal Pod Autoscaler
- `include_storage` (bool, default: false): Include persistent storage

#### 5. `generate_microservices_diagram`
Generate a microservices architecture diagram.

**Parameters:**
- `title` (str, default: "Microservices Architecture"): The title of the diagram
- `provider` (str, default: "aws"): Cloud provider (aws, azure, gcp)
- `services` (List[str], optional): List of microservice names
- `include_gateway` (bool, default: true): Include API Gateway
- `include_database` (bool, default: true): Include databases
- `include_cache` (bool, default: true): Include caching layer
- `include_queue` (bool, default: true): Include message queue

#### 6. `list_available_components`
List all available components that can be used in diagrams.

**Returns:** Dictionary with all available providers, categories, and components.

## Component Types

Components are specified using a dot notation: `provider.category.component`

### AWS Components
- **Compute**: `aws.compute.ec2`, `aws.compute.ecs`, `aws.compute.eks`, `aws.compute.lambda`
- **Database**: `aws.database.rds`, `aws.database.dynamodb`, `aws.database.elasticache`, `aws.database.redshift`
- **Network**: `aws.network.elb`, `aws.network.route53`, `aws.network.vpc`, `aws.network.igw`
- **Storage**: `aws.storage.s3`
- **Integration**: `aws.integration.sqs`, `aws.integration.sns`

### Azure Components
- **Compute**: `azure.compute.vm`, `azure.compute.aci`, `azure.compute.aks`, `azure.compute.functions`
- **Database**: `azure.database.sql`, `azure.database.cosmosdb`, `azure.database.redis`
- **Network**: `azure.network.lb`, `azure.network.appgw`, `azure.network.vnet`
- **Storage**: `azure.storage.storage`, `azure.storage.blob`
- **Integration**: `azure.integration.servicebus`, `azure.integration.eventgrid`

### GCP Components
- **Compute**: `gcp.compute.gce`, `gcp.compute.gke`, `gcp.compute.functions`
- **Database**: `gcp.database.sql`, `gcp.database.bigquery`, `gcp.database.firestore`
- **Network**: `gcp.network.lb`, `gcp.network.dns`
- **Storage**: `gcp.storage.gcs`
- **Analytics**: `gcp.analytics.pubsub`, `gcp.analytics.dataflow`

### Kubernetes Components
- **Compute**: `k8s.compute.pod`, `k8s.compute.deployment`, `k8s.compute.statefulset`, `k8s.compute.replicaset`
- **Network**: `k8s.network.service`, `k8s.network.ingress`
- **Storage**: `k8s.storage.pv`, `k8s.storage.pvc`
- **Config**: `k8s.config.hpa`

### On-Premises Components
- **Compute**: `onprem.compute.server`
- **Database**: `onprem.database.postgresql`, `onprem.database.mysql`, `onprem.database.mongodb`
- **Network**: `onprem.network.nginx`, `onprem.network.apache`
- **Memory**: `onprem.memory.redis`
- **Queue**: `onprem.queue.kafka`, `onprem.queue.rabbitmq`
- **Monitoring**: `onprem.monitoring.prometheus`, `onprem.monitoring.grafana`

## Examples

### Simple Web Architecture
```python
components = [
    {"id": "web", "type": "aws.compute.ec2", "label": "Web Server"},
    {"id": "db", "type": "aws.database.rds", "label": "Database"},
    {"id": "cache", "type": "aws.database.elasticache", "label": "Cache"}
]

connections = [
    {"from": "web", "to": "db", "label": "queries"},
    {"from": "web", "to": "cache", "label": "cache"}
]
```

### Clustered Architecture
```python
clusters = [
    {
        "name": "Web Tier",
        "components": [
            {"id": "web1", "type": "aws.compute.ec2", "label": "Web Server 1"},
            {"id": "web2", "type": "aws.compute.ec2", "label": "Web Server 2"}
        ]
    },
    {
        "name": "Database Tier",
        "components": [
            {"id": "db1", "type": "aws.database.rds", "label": "Primary DB"}
        ]
    }
]
```

## Testing

Run the test suite to verify the server functionality:

```bash
python test_server.py
```

The test will:
1. Check if Graphviz is installed
2. Test all diagram generation functions
3. Save generated diagrams to a `test_outputs` directory
4. Provide a summary of test results

## Integration with Architecture Squad

This MCP server is designed to work with the Architecture Squad project. Agents can use these tools to generate visual diagrams based on their architectural recommendations.

### Example Integration

```python
from semantic_kernel.connectors.mcp import MCPStdioPlugin

# Connect to the diagram generator MCP server
async with MCPStdioPlugin(
    name="DiagramGenerator",
    description="Architecture diagram generation capabilities",
    command="python",
    args=["mcp-servers/diagram-generator/server.py"],
    load_tools=True,
    load_prompts=False,
    request_timeout=30
) as mcp_plugin:
    kernel.add_plugin(mcp_plugin)
```

## Output Format

All diagram generation functions return a dictionary with:

```json
{
    "success": true,
    "title": "Diagram Title",
    "format": "png",
    "image_base64": "base64_encoded_image_data",
    "message": "Success message",
    "components_count": 3,
    "connections_count": 2
}
```

The `image_base64` field contains the diagram as a base64-encoded string that can be decoded and saved as an image file or displayed in web interfaces.

## Troubleshooting

### Common Issues

1. **Graphviz not found**: Install Graphviz and ensure it's in your system PATH
2. **Import errors**: Install all required dependencies using pip
3. **Empty diagrams**: Check that component types are correctly specified
4. **Connection errors**: Ensure component IDs match between components and connections

### Debug Mode

Set the logging level to DEBUG for more detailed output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

This MCP server is part of the Architecture Squad Demo project and follows the same licensing terms.
