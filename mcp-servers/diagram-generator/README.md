# Architecture Diagram Generator MCP Server

This MCP server provides programmatic tools for generating cloud and hybrid architecture diagrams using the [diagrams](https://diagrams.mingrammer.com/) library. It is designed for integration with AI agents and supports AWS, Azure, GCP, Kubernetes, and On-Premises components.

## Project Structure

```
mcp-servers/diagram-generator/
├── server.py            # Main MCP server entry point
├── requirements.txt     # Python dependencies
├── README.md            # This documentation
├── Dockerfile           # (Optional) Container build
├── test_all.py          # Test suite
├── core/                # Core diagram logic
├── diagram_generators/  # Modular diagram templates
├── tests/               # Unit/integration tests
└── ...
```

## Features

- **Simple Diagrams**: Generate basic architecture diagrams from component and connection lists
- **Clustered Diagrams**: Group components into logical clusters (tiers, environments, etc.)
- **Template Diagrams**: Pre-built templates for common architectures (AWS web apps, Kubernetes, microservices)
- **Multi-Cloud Support**: AWS, Azure, GCP, Kubernetes, On-Premises
- **Flexible Output**: PNG, JPG, SVG, or PDF
- **Base64 Encoding**: Returns diagrams as base64-encoded strings for easy integration

## Prerequisites

- Python 3.7 or higher
- [Graphviz](https://graphviz.gitlab.io/download/) (required by the diagrams library)

### Install Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get update && sudo apt-get install graphviz
```
**macOS (Homebrew):**
```bash
brew install graphviz
```
**Windows:**
- With Chocolatey: `choco install graphviz`
- Or download from [Graphviz website](https://graphviz.gitlab.io/download/)

## Installation

1. Install Python dependencies:
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

Or with Docker (if Dockerfile is present):
```bash
docker build -t diagram-generator .
docker run --rm -p 8002:8002 diagram-generator
```

### Environment Variables
If required, copy `.env.example` to `.env` and set any needed variables.

## Available Tools

All tools are exposed via the MCP protocol. Example tool signatures:

### 1. `generate_simple_diagram`
Create a basic architecture diagram.
- **Parameters:**
  - `title` (str)
  - `components` (List[Dict]): e.g. `[{"id": "web1", "type": "aws.compute.ec2", "label": "Web Server"}]`
  - `connections` (List[Dict], optional): e.g. `[{"from": "web1", "to": "db1", "label": "queries"}]`
  - `output_format` (str, default: "png")
  - `direction` (str, default: "TB")
  - `show_labels` (bool, default: true)

### 2. `generate_clustered_diagram`
Group components into clusters.
- **Parameters:**
  - `title` (str)
  - `clusters` (List[Dict]): e.g. `[{"name": "Web Tier", "components": [...] }]`
  - `connections` (List[Dict], optional)
  - `output_format`, `direction` (see above)

### 3. `generate_aws_web_app_diagram`
Predefined AWS web application architecture.
- **Parameters:**
  - `title` (str, default: "AWS Web Application")
  - `include_cdn`, `include_cache`, `include_monitoring`, `multi_az` (bool)

### 4. `generate_kubernetes_diagram`
Predefined Kubernetes architecture.
- **Parameters:**
  - `title` (str, default: "Kubernetes Architecture")
  - `replicas` (int)
  - `include_ingress`, `include_hpa`, `include_storage` (bool)

### 5. `generate_microservices_diagram`
Microservices architecture diagram.
- **Parameters:**
  - `title` (str, default: "Microservices Architecture")
  - `provider` (str: aws|azure|gcp)
  - `services` (List[str], optional)
  - `include_gateway`, `include_database`, `include_cache`, `include_queue` (bool)

### 6. `list_available_components`
Returns all supported component types as a dictionary.

## Component Types

Use dot notation: `provider.category.component` (see `list_available_components` for full list).

- **AWS**: `aws.compute.ec2`, `aws.database.rds`, ...
- **Azure**: `azure.compute.vm`, `azure.database.sql`, ...
- **GCP**: `gcp.compute.gce`, `gcp.database.sql`, ...
- **Kubernetes**: `k8s.compute.pod`, ...
- **On-Premises**: `onprem.compute.server`, ...

## Example Payloads

**Simple Web Architecture:**
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

**Clustered Architecture:**
```python
clusters = [
    {"name": "Web Tier", "components": [
        {"id": "web1", "type": "aws.compute.ec2", "label": "Web Server 1"},
        {"id": "web2", "type": "aws.compute.ec2", "label": "Web Server 2"}
    ]},
    {"name": "Database Tier", "components": [
        {"id": "db1", "type": "aws.database.rds", "label": "Primary DB"}
    ]}
]
```

## Output Format

All diagram generation tools return a dictionary:
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

- `image_base64` is a base64-encoded image (decode to save or display)

## Testing

Run the test suite to verify functionality:
```bash
python test_all.py
```
- Checks Graphviz installation
- Tests all diagram generation functions
- Saves diagrams to `test_outputs/`
- Prints summary of results

## Integration Example

Integrate with Semantic Kernel agents:
```python
from semantic_kernel.connectors.mcp import MCPStdioPlugin
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

## Troubleshooting

- **Graphviz not found**: Install Graphviz and ensure it's in your PATH
- **Import errors**: Run `pip install -r requirements.txt`
- **Empty diagrams**: Check component types and IDs
- **Connection errors**: Ensure IDs match between components and connections
- **Debugging**: Set logging to DEBUG for verbose output:
  ```python
  import logging
  logging.basicConfig(level=logging.DEBUG)
  ```

## License

This MCP server is part of the Architecture Squad Demo project and follows the same licensing terms.
