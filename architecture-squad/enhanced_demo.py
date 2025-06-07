#!/usr/bin/env python3
"""
Enhanced Architecture Squad Demo with improved agent coordination
"""

import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies import KernelFunctionSelectionStrategy, KernelFunctionTerminationStrategy
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelFunctionFromPrompt
from openai import AsyncOpenAI
from dotenv import load_dotenv


def create_kernel() -> Kernel:
    """Create a kernel with chat completion service"""
    load_dotenv()

    kernel = Kernel()
    client = AsyncOpenAI(
        api_key=os.getenv("GITHUB_TOKEN"),
        base_url="https://models.inference.ai.azure.com"
    )
    chat_completion = OpenAIChatCompletion(
        ai_model_id=os.getenv("GITHUB_MODEL", "gpt-4o"),
        async_client=client
    )
    kernel.add_service(chat_completion)
    return kernel


def create_solution_architect(kernel: Kernel) -> ChatCompletionAgent:
    """Create the Solution Architect agent"""
    return ChatCompletionAgent(
        kernel=kernel,
        name="Solution_Architect",
        instructions="""
You are a Solution Architect responsible for high-level system design and architectural patterns.
Your responsibility is to analyze user requirements and provide high-level architectural solutions.

When a user provides system requirements:
- Identify the core business objectives and functional requirements
- Recommend appropriate architectural patterns (microservices, monolith, serverless, etc.)
- Define high-level system components and their relationships
- Consider scalability, performance, and reliability requirements
- Provide architectural principles and design decisions

RULES:
- Focus on business value and solution fit
- Consider trade-offs between different architectural approaches
- Ensure alignment with industry best practices
- Structure your response with clear sections and bullet points
- Keep responses comprehensive but not overly detailed
- When finished, clearly state "Technical_Architect should provide detailed technical specifications"
""",
    )


def create_technical_architect(kernel: Kernel) -> ChatCompletionAgent:
    """Create the Technical Architect agent"""
    return ChatCompletionAgent(
        kernel=kernel,
        name="Technical_Architect",
        instructions="""
You are a Technical Architect responsible for detailed technical specifications and implementation guidance.
Your responsibility is to translate high-level architecture into specific technical requirements.

When reviewing Solution Architect's design:
- Define specific technologies, frameworks, and tools
- Specify API designs and communication protocols
- Detail database schemas and data models
- Define deployment and infrastructure requirements
- Provide implementation roadmap and milestones

RULES:
- Be specific about technology choices and justify them
- Include performance and scalability considerations
- Address integration patterns and data flow
- Structure technical specifications clearly
- When finished, clearly state "Security_Architect should review security aspects"
""",
    )


def create_security_architect(kernel: Kernel) -> ChatCompletionAgent:
    """Create the Security Architect agent"""
    return ChatCompletionAgent(
        kernel=kernel,
        name="Security_Architect",
        instructions="""
You are a Security Architect responsible for security design and compliance.
Your responsibility is to ensure the architecture addresses security requirements and best practices.

When reviewing the architecture:
- Identify security risks and vulnerabilities
- Recommend security controls and measures
- Address authentication, authorization, and data protection
- Consider compliance requirements and industry standards
- Provide security implementation guidance

RULES:
- Focus on practical security measures
- Address both technical and operational security
- Consider security throughout the development lifecycle
- Structure security recommendations clearly
- When finished, clearly state "Data_Architect should design data architecture"
""",
    )


def create_data_architect(kernel: Kernel) -> ChatCompletionAgent:
    """Create the Data Architect agent"""
    return ChatCompletionAgent(
        kernel=kernel,
        name="Data_Architect",
        instructions="""
You are a Data Architect responsible for data strategy and storage design.
Your responsibility is to design data architecture and data flow patterns.

When reviewing the architecture:
- Define data models and database schemas
- Design data flow and integration patterns
- Address data storage, backup, and recovery strategies
- Consider data governance and quality measures
- Recommend data processing and analytics approaches

RULES:
- Focus on data consistency and integrity
- Address scalability and performance of data operations
- Consider data privacy and compliance requirements
- Structure data architecture recommendations clearly
- When finished, clearly state "Documentation_Specialist should create comprehensive documentation"
""",
    )


def create_documentation_specialist(kernel: Kernel) -> ChatCompletionAgent:
    """Create the Documentation Specialist agent"""
    return ChatCompletionAgent(
        kernel=kernel,
        name="Documentation_Specialist",
        instructions="""
You are a Documentation Specialist responsible for creating comprehensive technical documentation.
Your responsibility is to compile all architectural decisions into a clear, actionable document.

When reviewing all previous inputs:
- Create a comprehensive architecture document
- Include executive summary, system overview, and technical specifications
- Document all architectural decisions and rationale
- Provide implementation guidance and next steps
- Ensure documentation is clear and actionable

RULES:
- Structure the document professionally with clear sections
- Include all important architectural decisions from previous agents
- Make it accessible to both technical and business stakeholders
- Provide actionable implementation steps
- End with "ARCHITECTURE DOCUMENT COMPLETE" when finished
""",
    )


def create_selection_function() -> KernelFunctionFromPrompt:
    """Create the agent selection function"""
    return KernelFunctionFromPrompt(
        function_name="selection",
        prompt="""
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
- If RESPONSE is from Solution_Architect, move to Technical_Architect
- If RESPONSE is from Technical_Architect, move to Security_Architect
- If RESPONSE is from Security_Architect, move to Data_Architect
- If RESPONSE is from Data_Architect, move to Documentation_Specialist
- Follow the natural flow: Solution → Technical → Security → Data → Documentation

RESPONSE:
{{$lastmessage}}
""",
    )


def create_termination_function() -> KernelFunctionFromPrompt:
    """Create the termination function"""
    return KernelFunctionFromPrompt(
        function_name="termination",
        prompt="""
Examine the RESPONSE and determine if the architecture document is complete.
If the response contains "ARCHITECTURE DOCUMENT COMPLETE", respond: COMPLETE
Otherwise respond: CONTINUE

RESPONSE:
{{$lastmessage}}
""",
    )


async def enhanced_demo():
    """Run an enhanced demo with proper agent coordination"""
    print("🏗️  Enhanced Architecture Squad Demo")
    print("=" * 60)

    # Create kernel and agents
    kernel = create_kernel()
    solution_architect = create_solution_architect(kernel)
    technical_architect = create_technical_architect(kernel)
    security_architect = create_security_architect(kernel)
    data_architect = create_data_architect(kernel)
    documentation_specialist = create_documentation_specialist(kernel)

    # Create selection and termination functions
    selection_function = create_selection_function()
    termination_function = create_termination_function()

    # Create enhanced group chat with strategies
    chat = AgentGroupChat(
        agents=[
            solution_architect,
            technical_architect,
            security_architect,
            data_architect,
            documentation_specialist
        ],
        selection_strategy=KernelFunctionSelectionStrategy(
            initial_agent=solution_architect,
            function=selection_function,
            kernel=kernel,
            result_parser=lambda result: str(result.value[0]).strip(
            ) if result.value[0] else "Solution_Architect",
            history_variable_name="lastmessage",
        ),
        termination_strategy=KernelFunctionTerminationStrategy(
            agents=[documentation_specialist],
            function=termination_function,
            kernel=kernel,
            result_parser=lambda result: "COMPLETE" in str(
                result.value[0]).upper() if result.value[0] else False,
            history_variable_name="lastmessage",
            maximum_iterations=10,
        ),
    )

    print("✓ Enhanced Architecture Squad initialized with intelligent coordination")
    print("🤖 Team: Solution Architect → Technical Architect → Security Architect → Data Architect → Documentation Specialist")

    # Test requirement
    requirement = """
Design a real-time chat application with the following requirements:

Business Requirements:
- Support for direct messages and group chats
- File sharing capabilities (images, documents)
- Message history and search functionality
- User presence indicators (online/offline/away)
- Push notifications for mobile devices

Technical Requirements:
- Support 10,000 concurrent users
- Messages should be delivered within 100ms
- 99.9% uptime requirement
- GDPR compliance for EU users
- Mobile apps for iOS and Android
- Web application for desktop users

Integration Requirements:
- Single sign-on with corporate directory
- Integration with calendar systems
- API for third-party integrations
"""

    print(f"\n📋 Complex Requirement:\n{requirement}")
    print("\n" + "=" * 80)
    print("🤝 ENHANCED ARCHITECTURE SQUAD COLLABORATION")
    print("=" * 80)

    # Add user message and process
    await chat.add_chat_message(message=requirement)

    try:
        response_count = 0
        async for response in chat.invoke():
            if response:
                response_count += 1
                print(f"\n💭 {response.name} (Response {response_count}):")
                print("-" * 60)
                print(response.content)
                print("-" * 60)

                # Safety limit
                if response_count >= 8:
                    print("\n⚠️  Reached maximum responses limit")
                    break

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(enhanced_demo())
