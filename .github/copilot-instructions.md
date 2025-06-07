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
Built with **Model Context Protocol** - Create extensible plugins for agent capabilities.

#### MCP Server Guidelines
- Each server should focus on a specific capability (research, diagrams, analysis)
- Use standardized MCP protocol for tool registration
- Implement proper error handling and logging
- Follow async patterns for external API calls
- Include proper authentication and rate limiting

#### Example MCP Server Structure
```python
from mcp import McpServer, Tool

class ResearchMCP(McpServer):
    def __init__(self):
        super().__init__("research-server")
        self.register_tool(self.web_search)
        self.register_tool(self.analyze_documentation)
    
    @Tool("web_search")
    async def web_search(self, query: str) -> dict:
        # Implementation for web search capability
        pass
    
    @Tool("analyze_documentation")
    async def analyze_documentation(self, url: str) -> dict:
        # Implementation for documentation analysis
        pass
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
│   ├── research_server.py
│   ├── diagram_server.py
│   ├── analysis_server.py
│   ├── requirements.txt
│   └── .env
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
semantic-kernel
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
```
mcp
fastapi
uvicorn
requests
aiohttp
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
# In architecture-squad/agents/research_agent.py
from mcp_client import MCPClient

class ResearchAgent:
    def __init__(self, kernel, mcp_client: MCPClient):
        self.kernel = kernel
        self.mcp = mcp_client
    
    async def research_topic(self, topic: str):
        # Use MCP server for web research
        research_results = await self.mcp.call_tool("web_search", {"query": topic})
        return self.process_research_results(research_results)
```

This pattern enables collaborative architecture design through specialized AI agents working together across multiple integrated projects to produce comprehensive technical documentation.