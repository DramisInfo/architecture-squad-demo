# Architecture Squad Demo

A comprehensive demonstration of collaborative AI architect agents working together to produce detailed architecture documents. This repository contains multiple interconnected projects that showcase how specialized AI agents can collaborate through group chat patterns, web interfaces, and extensible plugin systems.

## Repository Structure

This repository contains three main components:

### 🤖 Architecture Squad (`/architecture-squad/`)
A multi-agent system using **Semantic Kernel** group chat patterns where different architect agents collaborate to:
- **Requirements Analysis**: Parse and understand project requirements
- **Solution Design**: Create architectural patterns and designs
- **Documentation Generation**: Produce detailed architecture documents
- **Review & Validation**: Cross-validate designs and ensure quality

### 🖥️ Chainlit UI (`/chainlit-ui/`)
A modern web interface built with **Chainlit** that provides:
- Interactive chat interface for communicating with the architecture squad
- Real-time collaboration visualization between agents
- Document preview and export capabilities
- Session management and history

### 🔌 MCP Servers (`/mcp-servers/`)
**Model Context Protocol (MCP)** servers that extend agent capabilities through plugins:
- **Research Plugin**: Web search and documentation analysis
- **Diagram Plugin**: Architecture diagram generation
- **Code Analysis Plugin**: Codebase analysis and recommendations
- **Compliance Plugin**: Security and regulatory compliance checking

## How It Works

The agents work together using Semantic Kernel's group chat functionality to simulate a real architecture team, with each agent bringing specialized expertise. The Chainlit interface provides an intuitive way to interact with the squad, while MCP servers add powerful plugin capabilities for enhanced functionality.

## Features

- **Multi-Agent Collaboration**: Agents with different architectural specializations
- **Document Generation**: Automated creation of detailed architecture documents
- **Interactive Workflow**: Agents communicate and build upon each other's work
- **Extensible Framework**: Easy to add new agent types and capabilities

## Getting Started

### Prerequisites

- Python 3.10+
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/architecture-squad-demo
   cd architecture-squad-demo
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Project Components

### Architecture Squad (Semantic Kernel)
The core multi-agent system uses Semantic Kernel's group chat patterns to orchestrate collaboration between specialized architect agents. Each project subdirectory contains:

- `/architecture-squad/` - Main Semantic Kernel group chat implementation
  - Agent definitions and specializations
  - Selection and termination strategies
  - Collaborative workflow management
  - Document generation pipelines

### Chainlit UI (Web Interface)
A modern web application that provides an intuitive interface for interacting with the architecture squad:

- `/chainlit-ui/` - Chainlit-based web interface
  - Real-time chat with the architecture squad
  - Agent collaboration visualization
  - Document preview and export
  - Session history and management

### MCP Servers (Agent Extensions)
Model Context Protocol servers that extend agent capabilities through specialized plugins:

- `/mcp-servers/` - MCP server implementations
  - Research and documentation analysis tools
  - Diagram generation capabilities
  - Code analysis and recommendations
  - Compliance and security checking

## Usage

Each component can be run independently or together as a complete system:

### Running Individual Components

1. **Architecture Squad Only**:
   ```bash
   cd architecture-squad
   python main.py
   ```

2. **Chainlit UI**:
   ```bash
   cd chainlit-ui
   chainlit run app.py
   ```

3. **MCP Servers**:
   ```bash
   cd mcp-servers
   python -m uvicorn server:app --reload
   ```

### Running the Complete System
*Instructions for orchestrating all components together will be added as development progresses.*

## Agent Types

The architecture squad includes specialized agents such as:

- **Solution Architect**: High-level system design and patterns
- **Technical Architect**: Detailed technical specifications
- **Security Architect**: Security considerations and compliance
- **Data Architect**: Data flow and storage design
- **Documentation Specialist**: Technical writing and formatting

## Example Output

The squad produces comprehensive architecture documents including:

- System overview and context
- Component diagrams and relationships
- Security and compliance considerations
- Deployment and operational guidance
- Technology stack recommendations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Inspiration

This project is inspired by the collaborative AI agent examples in the [Azure Samples Python AI Agent Frameworks Demos](https://github.com/Azure-Samples/python-ai-agent-frameworks-demos) repository.