# Documentation Specialist MCP Integration

This document describes the enhanced Documentation Specialist agent with integrated diagram generation capabilities through Model Context Protocol (MCP).

## Overview

The Documentation Specialist has been enhanced with visual diagram generation capabilities by integrating with the `diagram-generator` MCP server. This allows the agent to automatically create professional architecture diagrams while generating comprehensive technical documentation.

## Features

### Enhanced Capabilities
- **Automatic Diagram Generation**: Creates architecture diagrams based on input specifications
- **Multi-Cloud Support**: Supports AWS, Azure, GCP, Kubernetes, and on-premises components
- **Multiple Diagram Types**: Simple, clustered, web application, Kubernetes, and microservices diagrams
- **Professional Visualization**: Consistent styling and formatting for all diagrams
- **Seamless Integration**: Works within existing architecture squad workflows

### Available Diagram Tools
1. **generate_simple_diagram**: Basic architecture diagrams with components and connections
2. **generate_clustered_diagram**: Diagrams with grouped components (tiers, environments)
3. **generate_aws_web_app_diagram**: AWS-specific web application architectures
4. **generate_kubernetes_diagram**: Kubernetes cluster architecture diagrams
5. **generate_microservices_diagram**: Microservices architecture diagrams
6. **list_available_components**: List all available diagram components across providers

## Usage

### Basic Usage
```python
from utils.kernel import create_kernel
from agents.documentation_specialist import create_enhanced_documentation_specialist

# Create kernel
kernel = create_kernel()

# Create enhanced documentation specialist with MCP integration
doc_specialist = await create_enhanced_documentation_specialist(kernel)
```

### Fallback Usage
If MCP integration fails, the agent automatically falls back to the standard documentation specialist:

```python
from agents.documentation_specialist import create_documentation_specialist

# Fallback without MCP integration
doc_specialist = create_documentation_specialist(kernel)
```

## Integration Architecture

```
┌─────────────────────────────────────┐
│     Documentation Specialist       │
│           (Enhanced)                │
├─────────────────────────────────────┤
│  - Technical Documentation         │
│  - Reference Management            │
│  - Content Synthesis               │
│  + Diagram Generation (NEW)        │
└─────────────────┬───────────────────┘
                  │ MCP Connection
                  ▼
┌─────────────────────────────────────┐
│      Diagram Generator MCP          │
│            Server                   │
├─────────────────────────────────────┤
│  - Architecture Diagrams           │
│  - Multi-Cloud Components          │
│  - Professional Styling            │
│  - Multiple Output Formats         │
└─────────────────────────────────────┘
```

## Agent Instructions Enhancement

The enhanced agent includes specific instructions for diagram generation:

### When to Generate Diagrams
- Always generate at least one main architecture diagram
- Create specialized diagrams based on architecture type:
  - Web applications: Use `generate_aws_web_app_diagram` or `generate_clustered_diagram`
  - Microservices: Use `generate_microservices_diagram`
  - Container/K8s deployments: Use `generate_kubernetes_diagram`
  - Multi-tier systems: Use `generate_clustered_diagram`

### Diagram Integration in Documentation
- Include diagram descriptions and references in appropriate sections
- Reference diagrams by their generated titles in the document
- Explain what each diagram shows and its purpose
- Include diagram file paths or base64 references for embedding

## Technical Implementation

### MCP Server Connection
The agent connects to the diagram generator MCP server using:
- **Transport**: STDIO (subprocess communication)
- **Server Path**: `../../../mcp-servers/diagram-generator/server.py`
- **Plugin Name**: "DiagramGenerator"
- **Timeout**: 30 seconds
- **Load Tools**: True (diagram generation functions)
- **Load Prompts**: False (no additional prompts needed)

### Error Handling
- Automatic fallback to standard documentation specialist if MCP connection fails
- Comprehensive error logging for debugging
- Graceful degradation without breaking existing workflows

### Dependencies
- `semantic-kernel[mcp]`: Core MCP integration support
- `fastmcp`: MCP server framework (in diagram generator)
- `diagrams`: Python diagrams library (in diagram generator)

## Testing

Run the included tests to verify the integration:

```bash
# Test MCP integration
python test_mcp_integration.py

# View usage example
python example_enhanced_documentation.py

# Test diagram generator server directly
cd ../mcp-servers/diagram-generator
python test_server.py
```

## File Structure

```
architecture-squad/agents/
├── documentation_specialist.py          # Enhanced agent with MCP integration
├── test_mcp_integration.py             # MCP integration test
└── example_enhanced_documentation.py    # Usage example

mcp-servers/diagram-generator/
├── server.py                           # MCP server implementation
├── test_server.py                      # Server tests
├── requirements.txt                    # Server dependencies
└── README.md                          # Server documentation
```

## Benefits

1. **Automated Visualization**: No manual diagram creation needed
2. **Consistency**: Standardized diagram styling across projects
3. **Efficiency**: Faster documentation creation with visual aids
4. **Professional Quality**: High-quality architecture diagrams
5. **Integration**: Seamless workflow with existing agents
6. **Flexibility**: Multiple diagram types for different architectures
7. **Fallback**: Graceful degradation if MCP is unavailable

## Future Enhancements

- Additional diagram types (sequence, deployment, etc.)
- Custom styling and branding options
- Export to additional formats (SVG, PDF, etc.)
- Interactive diagram features
- Integration with other MCP servers for extended capabilities

---

**Note**: This enhancement maintains full backward compatibility with existing architecture squad workflows while adding powerful visual documentation capabilities.
