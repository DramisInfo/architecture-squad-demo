# Architecture Squad Demo - Certified Solution Architects

A comprehensive demonstration of collaborative AI architect agents working together to produce detailed architecture documents with visual diagrams. This repository showcases **certified solution architects** specialized in different cloud platforms (Azure, AWS, Kubernetes/OpenShift) who collaborate through Semantic Kernel group chat patterns to create professional enterprise architecture solutions.

## 🏗️ What's New: Enhanced Architecture Squad

The Architecture Squad has been significantly enhanced with certified specialists and visual diagram generation:

### 🎯 Certified Platform Specialists
- **🔍 Platform Selector** - Intelligently routes requirements to the appropriate cloud specialist based on requirements analysis and platform preferences
- **☁️ Azure Solution Architect** - Microsoft Azure certified expert with Azure Architecture Center integration, Azure Well-Architected Framework expertise, and Azure Red Hat OpenShift (ARO) specialization
- **🚀 AWS Solution Architect** - Amazon Web Services certified expert with AWS Well-Architected Framework expertise and Red Hat OpenShift Service on AWS (ROSA) specialization
- **🐳 Kubernetes Solution Architect** - Container orchestration & Red Hat OpenShift certified specialist for cloud-native architectures and enterprise Kubernetes platforms

### 🛠️ Technical Specialists  
- **🏛️ Solution Architect** - General high-level system design for platform-agnostic solutions and architectural patterns
- **⚙️ Technical Architect** - Detailed technical specifications, implementation guidance, and technology stack recommendations
- **🔒 Security Architect** - Security design, compliance frameworks, risk assessment, and OpenShift security integration
- **💾 Data Architect** - Data strategy, storage design, data flow architecture, and governance frameworks
- **📚 Documentation Specialist (Enhanced)** - Comprehensive technical documentation with **automated diagram generation** via MCP integration and visual architecture output

### 🎨 Visual Architecture Capabilities
- **Diagram Generation MCP Server** - Professional architecture diagrams using the `diagrams` library with modular, maintainable architecture
- **Multi-Cloud Component Support** - Extensive support for AWS, Azure, GCP, Kubernetes, and on-premises components
- **Multiple Diagram Types** - Simple, clustered, web application, Kubernetes, and microservices architecture templates
- **Flexible Output Formats** - PNG, SVG, PDF, and JPG with base64 encoding for seamless web integration
- **Template-Based Generation** - Pre-built architecture patterns for common enterprise scenarios

## Repository Structure

This repository contains three main components that work together to provide a comprehensive architecture design experience:

### 🤖 Architecture Squad (`/architecture-squad/`)
A multi-agent system using **Semantic Kernel** group chat patterns where certified architect agents collaborate to:
- **Intelligent Platform Routing**: Platform Selector analyzes requirements and routes to certified specialists (Azure, AWS, Kubernetes)
- **Requirements Analysis**: Parse and understand complex project requirements with cloud platform preferences
- **Specialized Solution Design**: Create platform-specific architectural patterns leveraging certified expertise
- **Collaborative Documentation**: Generate comprehensive, platform-optimized architecture documents
- **Best Practices Integration**: Each specialist brings certified knowledge and industry standards

**Key Agents:**
- Platform Selector with intelligent routing logic
- Azure Solution Architect (Azure Architecture Center integration)  
- AWS Solution Architect (AWS Well-Architected Framework, ROSA specialization)
- Kubernetes Solution Architect (OpenShift certified expertise)
- Enhanced Documentation Specialist with MCP diagram generation

### 🖥️ Chainlit UI (`/chainlit-ui/`)
A modern web interface built with **Chainlit** that provides:
- **Real-time Agent Collaboration**: Watch certified specialists discuss and build upon each other's work
- **Interactive Architecture Design**: Submit requirements and see platform-specific solutions emerge
- **Visual Diagram Integration**: Architecture diagrams generated automatically and displayed in real-time
- **Session Management**: Persistent conversations with export capabilities
- **Responsive Design**: Async workflows for fast, scalable interactions

### 🔌 MCP Servers (`/mcp-servers/`)
**Model Context Protocol (MCP)** servers that extend agent capabilities through specialized plugins:

#### Diagram Generator MCP Server (`/mcp-servers/diagram-generator/`)
- **Professional Architecture Diagrams**: Using the `diagrams` library for consistent, high-quality output
- **Multi-Cloud Component Library**: Extensive support for AWS, Azure, GCP, Kubernetes, and on-premises components
- **Multiple Diagram Types**: 
  - Simple component diagrams with connections
  - Clustered diagrams with logical groupings (tiers, environments)
  - Template-based diagrams (web applications, microservices, Kubernetes)
- **Flexible Output Formats**: PNG, SVG, PDF, JPG with base64 encoding
- **Modular Architecture**: Clean, maintainable codebase with comprehensive test coverage

**Additional Planned MCP Servers:**
- **Research Plugin**: Web search and documentation analysis
- **Code Analysis Plugin**: Codebase analysis and recommendations  
- **Compliance Plugin**: Security and regulatory compliance checking

## How It Works

The agents work together using Semantic Kernel's group chat functionality to simulate a real architecture team, with each agent bringing specialized expertise. The Chainlit interface provides an intuitive way to interact with the squad, while MCP servers add powerful plugin capabilities for enhanced functionality.

## 🚀 Features

- **🎯 Certified Platform Specialists**: Azure, AWS, and Kubernetes certified solution architects with real-world expertise
- **🔍 Intelligent Platform Routing**: Automatic selection of the best cloud specialist based on requirement analysis
- **🤝 Multi-Agent Collaboration**: Specialized agents working together with certified domain expertise
- **📋 Platform-Optimized Documentation**: Architecture documents tailored to your chosen cloud platform with best practices
- **🎨 Automated Diagram Generation**: Professional architecture diagrams created automatically via MCP server integration
- **🔧 Interactive Workflow**: Real-time collaboration between certified architects with visual feedback
- **🌐 Multi-Cloud Support**: Design solutions for Azure, AWS, Kubernetes, or platform-agnostic architectures
- **🛡️ Best Practices Integration**: Each specialist brings certified knowledge, reference architectures, and industry standards
- **📊 Visual Architecture Output**: High-quality diagrams in multiple formats (PNG, SVG, PDF) with multi-cloud component support
- **🏗️ Template-Based Design**: Pre-built architecture templates for common patterns (web apps, microservices, Kubernetes)
- **🔄 Async Performance**: Fast, responsive agent collaboration with persistent session management

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- **Graphviz** (required for diagram generation)
  - **Ubuntu/Debian**: `sudo apt-get install graphviz`
  - **macOS**: `brew install graphviz`
  - **Windows**: Download from [Graphviz website](https://graphviz.org/download/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/architecture-squad-demo
   cd architecture-squad-demo
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install requirements for all components:**
   
   **Architecture Squad (Core System):**
   ```bash
   cd architecture-squad
   pip install -r requirements.txt
   cd ..
   ```
   
   **Chainlit UI (Web Interface):**
   ```bash
   cd chainlit-ui
   pip install -r requirements.txt
   cd ..
   ```
   
   **Diagram Generator MCP Server:**
   ```bash
   cd mcp-servers/diagram-generator
   pip install -r requirements.txt
   cd ../..
   ```

### Configuration

The architecture squad supports multiple AI service providers through environment variables:

#### GitHub Models (Default)
```bash
API_HOST=github
GITHUB_TOKEN=your_github_token_here
GITHUB_MODEL=gpt-4o
```

#### Azure OpenAI with API Key
```bash
API_HOST=azure
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_CHAT_MODEL=gpt-4
AZURE_OPENAI_VERSION=2024-02-01
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
```

#### Azure OpenAI with Azure AD (Enterprise)
```bash
API_HOST=azure
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_CHAT_MODEL=gpt-4
AZURE_OPENAI_VERSION=2024-02-01
# Leave AZURE_OPENAI_API_KEY empty to use Azure AD authentication
# Requires: az login or service principal configuration
```

Copy `/architecture-squad/.env.example` to `/architecture-squad/.env` and update with your credentials.

## Project Components

### Architecture Squad (Semantic Kernel)
The core multi-agent system uses Semantic Kernel's group chat patterns to orchestrate collaboration between specialized architect agents. The project structure includes:

- `/architecture-squad/` - Main Semantic Kernel group chat implementation
  - `agents/` - Individual agent definitions with specialized expertise
  - `strategies/` - Selection and termination strategies for agent coordination
  - `utils/` - Kernel creation and group chat utilities
  - Demo scripts: `main.py`, `demo_certified_architects.py`, `automated_demo.py`
  - Test scripts: `test_certified_architects.py`, `test_documentation_specialist_mcp.py`
  - Setup validation: `validate_setup.py`

### Chainlit UI (Web Interface)
A modern web application that provides an intuitive interface for interacting with the architecture squad:

- `/chainlit-ui/` - Chainlit-based web interface
  - Real-time chat with the architecture squad
  - Agent collaboration visualization
  - Document preview and export
  - Session history and management

### MCP Servers (Agent Extensions)
Model Context Protocol servers that extend agent capabilities through specialized plugins:

- `/mcp-servers/diagram-generator/` - MCP server for diagram generation
  - `core/` - Core diagram generation logic
  - `diagram_generators/` - Specialized diagram templates
  - `tests/` - Comprehensive test suite
  - Professional architecture diagrams with multi-cloud support
  - Modular, maintainable architecture (see `ARCHITECTURE.md`)

## 🎯 Quick Start with Certified Solution Architects

### 1. Validate Setup
```bash
cd architecture-squad
python validate_setup.py
```

### 2. Run Interactive Demo with Certified Architects
```bash
cd architecture-squad
python demo_certified_architects.py
```

This demo showcases:
- **Azure Enterprise Solutions** - Microsoft ecosystem integration with ARO (Azure Red Hat OpenShift)
- **AWS Serverless Architectures** - Cost-optimized cloud-native solutions with ROSA (Red Hat OpenShift Service on AWS)
- **Kubernetes Multi-Cloud** - Container orchestration with Red Hat OpenShift and portability
- **Platform-Agnostic Recommendations** - When no platform preference is specified

### 3. Interactive Architecture Design
```bash
cd architecture-squad
python main.py
```

Try these example requests:
- *"Design a microservices e-commerce platform using Azure services"*
- *"Create a serverless data processing pipeline on AWS"*
- *"Design a cloud-native application using Kubernetes and OpenShift"*
- *"I need a scalable web application but not sure which cloud platform to use"*

### 4. Test Enhanced Documentation & Diagram Generation
```bash
cd architecture-squad
python test_documentation_specialist_mcp.py
```

### 5. Web Interface (Optional)
```bash
cd chainlit-ui
chainlit run app.py
```

Open your browser to `http://localhost:8000` to interact with the Architecture Squad through the web interface.

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

3. **Diagram Generator MCP Server** (for testing):
   ```bash
   cd mcp-servers/diagram-generator
   python server.py
   ```

### Testing & Development

**Test Certified Architects System:**
```bash
cd architecture-squad
python test_certified_architects.py
```

**Test MCP Integration:**
```bash
cd architecture-squad
python test_documentation_specialist_mcp.py
```

**Run Automated Demo:**
```bash
cd architecture-squad
python automated_demo.py
```

**Test Diagram Generation:**
```bash
cd mcp-servers/diagram-generator
python test_all.py
```

### Running the Complete System
The system components work together through MCP protocol and async communication patterns for comprehensive architecture design workflows.

## Agent Types

The architecture squad includes specialized agents with certified expertise:

### Core Specialists
- **Platform Selector**: Intelligent routing agent that analyzes requirements and routes to the appropriate cloud platform specialist
- **Solution Architect**: High-level system design and architectural patterns for platform-agnostic solutions
- **Technical Architect**: Detailed technical specifications and implementation guidance
- **Security Architect**: Security design, compliance frameworks, and risk assessment with OpenShift integration
- **Data Architect**: Data flow and storage design, data governance, and lifecycle management
- **Documentation Specialist (Enhanced)**: Technical writing and formatting with automated diagram generation via MCP integration

### Certified Platform Specialists
- **Azure Solution Architect**: Microsoft Azure certified expert with Azure Architecture Center integration and ARO specialization
- **AWS Solution Architect**: Amazon Web Services certified expert with AWS Well-Architected Framework and ROSA specialization  
- **Kubernetes Solution Architect**: Container orchestration and Red Hat OpenShift certified specialist for cloud-native architectures

## Example Output

The squad produces comprehensive architecture documents including:

- **Executive Summary**: High-level business context and architectural objectives
- **System Overview and Objectives**: Detailed project requirements and success criteria
- **Architecture Overview**: Platform-specific architectural patterns and design decisions
- **Component Architecture**: Detailed component diagrams and system relationships
- **Security Design**: Security patterns, compliance frameworks, and risk mitigation
- **Data Architecture**: Data flow diagrams, storage strategies, and governance
- **Technology Stack**: Platform-specific service recommendations and justifications
- **Deployment Guide**: Infrastructure setup and operational procedures
- **Operational Considerations**: Monitoring, scaling, and maintenance strategies
- **Visual Diagrams**: Professional architecture diagrams in multiple formats (PNG, SVG, PDF)
- **References and Resources**: Links to reference architectures, documentation, and best practices

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Inspiration

This project is inspired by the collaborative AI agent examples in the [Azure Samples Python AI Agent Frameworks Demos](https://github.com/Azure-Samples/python-ai-agent-frameworks-demos) repository.