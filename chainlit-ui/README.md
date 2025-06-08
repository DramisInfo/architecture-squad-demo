# Architecture Squad - Chainlit UI

Welcome to the **Architecture Squad** - your AI-powered team of specialized architect agents!

## What is Architecture Squad?

Architecture Squad is a multi-agent system built with Semantic Kernel that brings together specialized AI architects to collaboratively design comprehensive system architectures. Each agent has a specific expertise area and they work together to create detailed architecture documents—including visual diagrams.

## Meet Your Architecture Team

### 🎯 **Solution Architect**
- High-level system design and architectural patterns
- Technology stack recommendations
- System integration strategies

### ⚙️ **Technical Architect** 
- Detailed technical specifications
- Component design and interactions
- Performance and scalability considerations

### 🔒 **Security Architect**
- Security design patterns and best practices
- Compliance and regulatory requirements
- Threat modeling and risk assessment

### 📊 **Data Architect**
- Data flow and storage strategies
- Database design and data modeling
- Data governance and lifecycle management

### 📝 **Documentation Specialist (Enhanced)**
- Comprehensive technical documentation
- Architecture decision records
- Implementation guides and best practices
- **Diagram generation and visual output** (integrated with the Diagram Generator MCP server)

### ☁️ **Platform Specialists**
- **Azure Solution Architect** – Microsoft Azure certified expert
- **AWS Solution Architect** – Amazon Web Services certified expert
- **Kubernetes Solution Architect** – Container orchestration & OpenShift expert
- **Platform Selector** – Routes to the right cloud specialist

## How to Use

1. **Describe your system**: Tell us about the system you want to architect (optionally specify platform preferences)
2. **Watch the collaboration**: See our agents—including platform specialists—work together in real-time
3. **Get comprehensive results**: Receive detailed architecture documentation and diagrams

## Example Prompts

- "Design a microservices architecture for an e-commerce platform"
- "Create a secure cloud architecture for a healthcare application"
- "Design a real-time analytics system for IoT data"
- "Plan the architecture for a social media platform with 1M users"
- "Design a cloud-native application using Kubernetes and OpenShift"

## Features

- ✅ **Real-time agent collaboration** – Watch agents discuss and build upon each other's work
- ✅ **Specialized expertise** – Each agent contributes their domain knowledge
- ✅ **Comprehensive output** – Get complete architecture documentation
- ✅ **Interactive interface** – Easy-to-use web interface
- ✅ **Persistent sessions** – Continue conversations across interactions
- ✅ **Platform-aware design** – Platform Selector and cloud-certified specialists
- ✅ **Diagram generation** – Visual architecture diagrams generated via the Diagram Generator MCP server (PNG, SVG, etc.)
- ✅ **Async workflow** – Fast, responsive, and scalable agent collaboration

## Diagram Generation & Visual Output

The enhanced Documentation Specialist agent can generate architecture diagrams using the [Diagram Generator MCP server](../mcp-servers/diagram-generator/README.md). Diagrams are returned as base64-encoded images and displayed in the UI. Supported diagram types include:
- Simple component diagrams
- Clustered/tiers diagrams
- AWS, Azure, Kubernetes, and microservices templates

## Integration & Architecture

- **Multi-agent system**: Built with Semantic Kernel, using async group chat and agent handoff strategies
- **MCP server integration**: Connects to the Diagram Generator MCP server for visual output
- **Modular, scalable design**: Follows best practices for maintainability and extensibility (see [diagram-generator/ARCHITECTURE.md](../mcp-servers/diagram-generator/ARCHITECTURE.md))
- **Async session workflow**: Persistent, user-specific sessions with real-time updates

## Development & Testing

- Run `test_enhanced_integration.py` to verify that the enhanced Documentation Specialist and diagram generation are working as expected.
- See [diagram-generator/README.md](../mcp-servers/diagram-generator/README.md) for diagram server setup and troubleshooting.

## Troubleshooting

- **Graphviz not found**: Install Graphviz and ensure it's in your system PATH (required for diagram generation)
- **MCP server errors**: Ensure the Diagram Generator MCP server is running and accessible
- **Import errors**: Install all required dependencies using pip
- **Empty diagrams**: Check that component types are correctly specified

## Getting Started

Simply type your architecture requirements in the chat below and let our team of AI architects collaborate to design your system—including visual diagrams!
