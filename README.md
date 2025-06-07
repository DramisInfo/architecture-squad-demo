# Architecture Squad Demo - Certified Solution Architects

A comprehensive demonstration of collaborative AI architect agents working together to produce detailed architecture documents. This repository showcases **certified solution architects** specialized in different cloud platforms (Azure, AWS, Kubernetes/OpenShift) who collaborate through Semantic Kernel group chat patterns.

## 🏗️ What's New: Certified Solution Architects

The Architecture Squad now includes **platform-certified specialists** who provide expert-level guidance for specific cloud platforms:

### 🎯 Platform Specialists
- **🔍 Platform Selector** - Intelligently routes requirements to the appropriate cloud specialist
- **☁️ Azure Solution Architect** - Microsoft Azure certified expert with deep platform knowledge
- **🚀 AWS Solution Architect** - Amazon Web Services certified expert with comprehensive AWS expertise  
- **🐳 Kubernetes Solution Architect** - Container orchestration & OpenShift certified specialist

### 🛠️ Technical Specialists  
- **🏛️ Solution Architect** - General high-level system design for platform-agnostic solutions
- **⚙️ Technical Architect** - Detailed technical specifications and implementation guidance
- **🔒 Security Architect** - Security design, compliance, and risk assessment
- **💾 Data Architect** - Data strategy, storage design, and data flow architecture
- **📚 Documentation Specialist** - Comprehensive technical documentation and diagrams

## Repository Structure

This repository contains three main components:

### 🤖 Architecture Squad (`/architecture-squad/`)
A multi-agent system using **Semantic Kernel** group chat patterns where certified architect agents collaborate to:
- **Platform Analysis**: Intelligent routing to certified cloud specialists
- **Requirements Analysis**: Parse and understand project requirements  
- **Solution Design**: Create platform-specific architectural patterns and designs
- **Documentation Generation**: Produce detailed, platform-optimized architecture documents
- **Review & Validation**: Cross-validate designs and ensure cloud best practices

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

## 🚀 Features

- **🎯 Certified Platform Specialists**: Azure, AWS, and Kubernetes certified solution architects
- **🔍 Intelligent Platform Routing**: Automatic selection of the best cloud specialist for your requirements
- **🤝 Multi-Agent Collaboration**: Specialized agents working together with domain expertise
- **📋 Platform-Optimized Documentation**: Architecture documents tailored to your chosen cloud platform
- **🔧 Interactive Workflow**: Real-time collaboration between certified architects
- **🌐 Multi-Cloud Support**: Design solutions for Azure, AWS, Kubernetes, or platform-agnostic architectures
- **🛡️ Best Practices Integration**: Each specialist brings certified knowledge and industry best practices

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

## 🎯 Quick Start with Certified Solution Architects

### 1. Validate Setup
```bash
cd architecture-squad
python validate_setup.py
```

### 2. Run Interactive Demo
```bash
cd architecture-squad
python demo_certified_architects.py
```

This demo showcases:
- **Azure Enterprise Solutions** - Microsoft ecosystem integration
- **AWS Serverless Architectures** - Cost-optimized cloud-native solutions  
- **Kubernetes Multi-Cloud** - Container orchestration and portability
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

### 4. Web Interface (Optional)
```bash
cd chainlit-ui
chainlit run app.py
```

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