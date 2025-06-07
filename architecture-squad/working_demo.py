#!/usr/bin/env python3
"""
Working Architecture Squad Demo using current Semantic Kernel API
"""

import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIPromptExecutionSettings,
)
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
- Keep responses concise but comprehensive
- When finished, indicate that Technical_Architect should provide detailed specifications
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
- When finished, indicate that Security_Architect should review security aspects
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
- Include diagrams descriptions where appropriate
- Make it accessible to both technical and business stakeholders
- End with "ARCHITECTURE DOCUMENT COMPLETE" when finished
""",
    )


async def main():
    """Main function for the architecture squad demo"""
    print("🏗️  Architecture Squad Demo")
    print("=" * 50)

    # Create kernel and agents
    kernel = create_kernel()
    solution_architect = create_solution_architect(kernel)
    technical_architect = create_technical_architect(kernel)
    documentation_specialist = create_documentation_specialist(kernel)

    # Create simple group chat (without complex strategies for now)
    chat = AgentGroupChat(
        agents=[solution_architect, technical_architect,
                documentation_specialist]
    )

    print("✓ Architecture Squad initialized")
    print("Team: Solution Architect → Technical Architect → Documentation Specialist")
    print("\nProvide your system requirements:")

    while True:
        user_input = input("\nUser > ").strip()
        if not user_input or user_input.lower() == "exit":
            break

        print("\n" + "=" * 60)
        print("🤝 ARCHITECTURE SQUAD COLLABORATION")
        print("=" * 60)

        # Add user message
        await chat.add_chat_message(message=user_input)

        # Process through agents
        try:
            async for response in chat.invoke():
                if response:
                    print(f"\n💭 {response.name}:")
                    print("-" * 40)
                    print(response.content)
                    print("-" * 40)

                    # Check if documentation is complete
                    if "ARCHITECTURE DOCUMENT COMPLETE" in response.content:
                        print("\n✅ Architecture design completed!")
                        break

        except Exception as e:
            print(f"❌ Error: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())
