# GitHub Copilot Instructions for Architecture Squad Demo

## Project Overview
This is a multi-project repository demonstrating collaborative AI architect agents working together to produce comprehensive architecture documents. The repository contains three main components:

1. **Architecture Squad** (`/architecture-squad/`) - Semantic Kernel multi-agent system
2. **Chainlit UI** (`/chainlit-ui/`) - Web interface for agent interaction
3. **MCP Servers** (`/mcp-servers/`) - Model Context Protocol servers for agent extensions

Each component has its own technology stack but they work together to create a comprehensive architecture design experience.

## Repository Structure and Guidelines

### Architecture Squad Component (`/architecture-squad/`)
Built with **Semantic Kernel** - Follow the group chat pattern from Azure Samples for collaborative AI agents.

### Multi-Agent Architecture Pattern
Follow the Semantic Kernel group chat pattern from Azure Samples:
- Use `AgentGroupChat` with multiple specialized agents
- Implement `KernelFunctionSelectionStrategy` for agent coordination
- Use `KernelFunctionTerminationStrategy` for conversation completion
- Apply `ChatHistoryTruncationReducer` for memory management

### Agent Specializations
Create agents with distinct architectural roles:
- **Solution Architect**: High-level system design and patterns
- **Technical Architect**: Detailed technical specifications
- **Security Architect**: Security considerations and compliance
- **Data Architect**: Data flow and storage design
- **Documentation Specialist**: Technical writing and formatting

### Agent Instructions Pattern
Each agent should have:
```python
agent = ChatCompletionAgent(
    kernel=kernel,
    name="Agent_Name",
    instructions="""
Your responsibility is to [specific role description].
- [Specific rule 1]
- [Specific rule 2]
- [Specific rule 3]
""",
)
```

### MCP Plugin Integration with Agents
Follow Microsoft's [Semantic Kernel MCP plugin documentation](https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-mcp-plugins?pivots=programming-language-python) for proper integration:

#### Required Dependencies
Ensure `semantic-kernel[mcp]` is installed:
```bash
pip install semantic-kernel[mcp]
```

#### MCP Plugin Integration Pattern
```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.mcp import MCPStdioPlugin, MCPSsePlugin
from semantic_kernel.agents import ChatCompletionAgent

async def create_agent_with_mcp(kernel: Kernel) -> ChatCompletionAgent:
    """Create an agent with MCP server integration"""
    
    # Option 1: Connect to stdio-based MCP server
    async with MCPStdioPlugin(
        name="AzureResearch",
        description="Azure documentation research capabilities",
        command="python",
        args=["mcp-servers/azure-research/server.py"],
        env={},  # Environment variables if needed
        load_tools=True,
        load_prompts=False,
        request_timeout=30
    ) as mcp_plugin:
        kernel.add_plugin(mcp_plugin)
        
        # Option 2: Connect to HTTP/SSE-based MCP server
        # async with MCPSsePlugin(
        #     name="AzureResearch",
        #     description="Azure documentation research capabilities", 
        #     url="http://localhost:8080",
        #     load_tools=True,
        #     load_prompts=False,
        #     request_timeout=30
        # ) as mcp_plugin:
        #     kernel.add_plugin(mcp_plugin)
        
        agent = ChatCompletionAgent(
            kernel=kernel,
            name="Enhanced_Agent",
            instructions="""
            You have access to MCP tools for enhanced capabilities.
            Use the available tools when appropriate for your tasks.
            """,
        )
        
        return agent

# Manual connection management (alternative)
async def create_agent_manual_mcp():
    """Alternative approach with manual MCP connection management"""
    mcp_plugin = MCPStdioPlugin(
        name="AzureResearch",
        description="Azure documentation research capabilities",
        command="python",
        args=["mcp-servers/azure-research/server.py"],
    )
    
    await mcp_plugin.connect()
    
    kernel = Kernel()
    kernel.add_plugin(mcp_plugin)
    
    agent = ChatCompletionAgent(kernel=kernel, name="Enhanced_Agent")
    
    # Remember to close the connection later
    # await mcp_plugin.close()
    
    return agent, mcp_plugin
```

#### MCP Plugin Configuration Options
- **`load_tools`**: Set to `True` to load tools from MCP server (default: True)
- **`load_prompts`**: Set to `False` if MCP server has no prompts to avoid hanging (default: True)
- **`request_timeout`**: Timeout for MCP server requests in seconds (recommended: 30)
- **`env`**: Environment variables to pass to the MCP server process

### Chainlit UI Component (`/chainlit-ui/`)
Built with **Chainlit** - Create an interactive web interface for communicating with the architecture squad.

#### Chainlit Development Guidelines
- Use `@cl.on_message` for handling user inputs
- Implement `@cl.on_chat_start` for session initialization
- Use `cl.Message` for sending responses to users
- Implement real-time agent collaboration visualization
- Store chat history and allow session management

#### Example Chainlit Structure
```python
import chainlit as cl
from architecture_squad import ArchitectureSquad

@cl.on_chat_start
async def start():
    squad = ArchitectureSquad()
    cl.user_session.set("squad", squad)
    await cl.Message(content="Welcome to the Architecture Squad! How can we help you design your system?").send()

@cl.on_message
async def main(message: cl.Message):
    squad = cl.user_session.get("squad")
    response = await squad.process_message(message.content)
    await cl.Message(content=response).send()
```

### MCP Servers Component (`/mcp-servers/`)
Built with **Model Context Protocol** - Create extensible plugins for agent capabilities following the [official MCP server quickstart guide](https://modelcontextprotocol.io/quickstart/server).

#### MCP Server Organization Guidelines
- **Each MCP server MUST be in its own dedicated folder** under `/mcp-servers/`
- Each server folder contains its own `requirements.txt`, `README.md`, and standalone test files
- Server folders should be named descriptively (e.g., `azure-research/`, `diagram-generator/`, `code-analyzer/`)
- Each server must be independently testable and deployable
- Follow the official MCP protocol specifications from https://modelcontextprotocol.io/

#### MCP Server Structure (Per Server Folder)
```
mcp-servers/
├── azure-research/
│   ├── server.py              # Main MCP server implementation
│   ├── test_server.py         # Standalone tests for the server
│   ├── requirements.txt       # Server-specific dependencies
│   ├── README.md             # Server documentation and usage
│   └── .env.example          # Environment variables template
├── diagram-generator/
│   ├── server.py
│   ├── test_server.py
│   ├── requirements.txt
│   ├── README.md
│   └── .env.example
└── code-analyzer/
    ├── server.py
    ├── test_server.py
    ├── requirements.txt
    ├── README.md
    └── .env.example
```

#### MCP Server Development Guidelines
- **Follow MCP Protocol**: Reference https://modelcontextprotocol.io/quickstart/server for implementation patterns
- **Use FastMCP Framework**: Recommended for Python-based MCP servers (simpler than raw MCP protocol)
- **Tool Registration**: Each server should focus on a specific capability (research, diagrams, analysis)
- **Standalone Testing**: Each server must include `test_server.py` for independent validation
- **Error Handling**: Implement proper error handling and logging for all MCP operations
- **Async Patterns**: Follow async patterns for external API calls and I/O operations
- **Authentication**: Include proper authentication and rate limiting where needed
- **Documentation**: Each server folder must have comprehensive README.md with usage examples

#### Example MCP Server Implementation (using FastMCP)
```python
# In mcp-servers/azure-research/server.py
from fastmcp import FastMCP
from typing import Dict, Any
import asyncio

# Create MCP server
mcp = FastMCP("Azure Research Server")

@mcp.tool()
async def search_azure_docs(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search Azure documentation for relevant information"""
    # Implementation for Azure documentation search
    return {
        "success": True,
        "query": query,
        "results": []
    }

@mcp.tool()
async def get_azure_service_info(service_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific Azure service"""
    # Implementation for service information retrieval
    return {
        "success": True,
        "service": service_name,
        "info": {}
    }

if __name__ == "__main__":
    mcp.run()
```

#### Standalone Testing Pattern
```python
# In mcp-servers/azure-research/test_server.py
import asyncio
import pytest
from server import search_azure_docs, get_azure_service_info

async def test_search_azure_docs():
    """Test Azure documentation search functionality"""
    result = await search_azure_docs("App Service", max_results=3)
    assert result["success"] is True
    assert "query" in result
    print("✅ Azure docs search test passed")

async def test_get_azure_service_info():
    """Test Azure service information retrieval"""
    result = await get_azure_service_info("Functions")
    assert result["success"] is True
    assert result["service"] == "Functions"
    print("✅ Azure service info test passed")

async def main():
    """Run all tests for the Azure Research MCP server"""
    print("🧪 Testing Azure Research MCP Server...")
    await test_search_azure_docs()
    await test_get_azure_service_info()
    print("✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())
```

## Multi-Project Integration Guidelines

### Communication Between Components
- **Architecture Squad ↔ Chainlit**: Use async messaging patterns
- **Architecture Squad ↔ MCP Servers**: Use MCP protocol for tool calls
- **Chainlit ↔ MCP Servers**: Indirect through Architecture Squad

### Environment Configuration
Support different configurations for each component:
```python
# In architecture-squad/.env
API_HOST=github  # or azure
GITHUB_TOKEN=your_token
GITHUB_MODEL=gpt-4o

# In chainlit-ui/.env
CHAINLIT_HOST=localhost
CHAINLIT_PORT=8000
SQUAD_API_URL=http://localhost:8001

# In mcp-servers/.env
MCP_PORT=8002
RESEARCH_API_KEY=your_key
```

### Project Structure
```
architecture-squad-demo/
├── architecture-squad/
│   ├── agents/
│   ├── strategies/
│   ├── utils/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
├── chainlit-ui/
│   ├── app.py
│   ├── components/
│   ├── static/
│   ├── requirements.txt
│   └── .env
├── mcp-servers/
│   ├── azure-research/
│   │   ├── server.py
│   │   ├── test_server.py
│   │   ├── requirements.txt
│   │   ├── README.md
│   │   └── .env.example
│   ├── diagram-generator/
│   │   ├── server.py
│   │   ├── test_server.py
│   │   ├── requirements.txt
│   │   ├── README.md
│   │   └── .env.example
│   └── code-analyzer/
│       ├── server.py
│       ├── test_server.py
│       ├── requirements.txt
│       ├── README.md
│       └── .env.example
└── README.md
```

### Group Chat Configuration
Implement collaborative workflow:
```python
chat = AgentGroupChat(
    agents=[agent1, agent2, agent3],
    selection_strategy=KernelFunctionSelectionStrategy(
        initial_agent=initial_agent,
        function=selection_function,
        kernel=kernel,
        result_parser=lambda result: str(result.value[0]).strip(),
        history_variable_name="lastmessage",
        history_reducer=history_reducer,
    ),
    termination_strategy=KernelFunctionTerminationStrategy(
        agents=[review_agent],
        function=termination_function,
        kernel=kernel,
        result_parser=lambda result: "COMPLETE" in str(result.value[0]).upper(),
        history_variable_name="lastmessage",
        maximum_iterations=20,
        history_reducer=history_reducer,
    ),
)
```

### Selection Function Pattern
Use prompts to control agent handoffs:
```python
selection_function = KernelFunctionFromPrompt(
    function_name="selection",
    prompt=f"""
Examine the RESPONSE and choose the next architect agent.
State only the agent name without explanation.

Choose from:
- Solution_Architect
- Technical_Architect  
- Security_Architect
- Data_Architect
- Documentation_Specialist

Rules:
- If RESPONSE is user requirements, start with Solution_Architect
- If RESPONSE is high-level design, move to Technical_Architect
- If RESPONSE is technical specs, move to Security_Architect
- Continue the collaboration pattern...

RESPONSE:
{{{{$lastmessage}}}}
""",
)
```

### Termination Strategy
Implement completion detection:
```python
termination_function = KernelFunctionFromPrompt(
    function_name="termination",
    prompt=f"""
Examine the RESPONSE and determine if the architecture document is complete.
If complete with all sections (overview, components, security, data, deployment), respond: COMPLETE
Otherwise respond: CONTINUE

RESPONSE:
{{{{$lastmessage}}}}
""",
)
```

### Environment Setup
Support both GitHub Models and Azure OpenAI:
```python
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "github":
    client = AsyncOpenAI(
        api_key=os.environ["GITHUB_TOKEN"], 
        base_url="https://models.inference.ai.azure.com"
    )
    model_id = os.getenv("GITHUB_MODEL", "gpt-4o")
elif API_HOST == "azure":
    # Azure OpenAI configuration
```

### Code Organization
Structure the project following the Azure Samples pattern:
- `examples/` - Demo implementations
- `agents/` - Agent definitions and roles
- `strategies/` - Selection and termination strategies
- `utils/` - Helper functions and utilities
- `.env` - Environment configuration
- `requirements.txt` - Dependencies

### Documentation Output
Generate comprehensive architecture documents including:
- **System Overview**: Context and objectives
- **Component Architecture**: System components and relationships
- **Security Design**: Security patterns and compliance
- **Data Architecture**: Data flow and storage strategies
- **Deployment Guide**: Infrastructure and operational guidance
- **Technology Stack**: Recommended tools and frameworks

### Best Practices
1. **Agent Coordination**: Use clear handoff signals between agents
2. **Memory Management**: Implement history truncation to manage context
3. **Error Handling**: Include robust error handling in agent interactions
4. **Async Operations**: Use async/await patterns for all agent operations
5. **Logging**: Include rich logging for debugging collaboration flows
6. **Testing**: Create unit tests for individual agents and integration tests for workflows

### Dependencies

#### Architecture Squad (`/architecture-squad/requirements.txt`)
```
semantic-kernel[mcp]
openai
azure-identity
python-dotenv
rich
asyncio
pydantic
```

#### Chainlit UI (`/chainlit-ui/requirements.txt`)
```
chainlit
requests
asyncio
python-dotenv
websockets
```

#### MCP Servers (`/mcp-servers/requirements.txt`)  
**Note**: Each MCP server folder has its own `requirements.txt` for server-specific dependencies
```
# Global MCP dependencies (if any shared across servers)
mcp
```

#### Individual MCP Server Dependencies
```
# Example: mcp-servers/azure-research/requirements.txt
mcp
aiohttp
beautifulsoup4
python-dotenv

# Example: mcp-servers/diagram-generator/requirements.txt  
mcp
pillow
matplotlib
python-dotenv
```

### Example Usage Pattern

#### Architecture Squad Standalone
```python
# In architecture-squad/main.py
async def main():
    kernel = create_kernel()
    
    # Create architecture squad
    solution_architect = create_solution_architect(kernel)
    technical_architect = create_technical_architect(kernel)
    security_architect = create_security_architect(kernel)
    
    # Setup group chat
    chat = create_architecture_group_chat([
        solution_architect, 
        technical_architect, 
        security_architect
    ])
    
    # Process architecture request
    user_input = "Design a microservices architecture for an e-commerce platform"
    await chat.add_chat_message(message=user_input)
    
    async for response in chat.invoke():
        if response:
            print(f"# {response.name.upper()}:\n{response.content}")
```

#### Chainlit Integration
```python
# In chainlit-ui/app.py
import chainlit as cl
from architecture_squad.main import ArchitectureSquad

@cl.on_chat_start
async def start():
    squad = ArchitectureSquad()
    cl.user_session.set("squad", squad)
    await cl.Message(content="Welcome to the Architecture Squad!").send()

@cl.on_message
async def main(message: cl.Message):
    squad = cl.user_session.get("squad")
    
    # Stream agent responses in real-time
    async for agent_response in squad.process_message(message.content):
        await cl.Message(
            content=agent_response.content,
            author=agent_response.agent_name
        ).send()
```

#### MCP Server Integration
```python
# In architecture-squad/agents/azure_solution_architect.py
from semantic_kernel import Kernel
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.agents import ChatCompletionAgent

async def create_azure_solution_architect_with_mcp(kernel: Kernel) -> ChatCompletionAgent:
    """Create Azure Solution Architect with MCP research capabilities"""
    
    # Connect to Azure Research MCP server
    async with MCPStdioPlugin(
        name="AzureResearch",
        description="Azure documentation research capabilities",
        command="python",
        args=["mcp-servers/azure-research/server.py"],
        load_tools=True,
        load_prompts=False,
        request_timeout=30
    ) as mcp_plugin:
        kernel.add_plugin(mcp_plugin)
        
        agent = ChatCompletionAgent(
            kernel=kernel,
            name="Azure_Solution_Architect",
            instructions="""
            You are a Microsoft Azure Certified Solution Architect with access to real-time Azure research tools.
            Use the available MCP tools to research Azure services and reference architectures.
            """,
        )
        
        return agent
```

This pattern enables collaborative architecture design through specialized AI agents working together across multiple integrated projects to produce comprehensive technical documentation.