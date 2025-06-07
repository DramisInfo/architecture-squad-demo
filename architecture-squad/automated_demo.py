#!/usr/bin/env python3
"""
Automated Architecture Squad Demo for testing
"""

import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
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
You are a Solution Architect. Analyze requirements and provide high-level architecture.
Keep responses concise. End with "→ Technical_Architect should provide detailed specs."
""",
    )


def create_technical_architect(kernel: Kernel) -> ChatCompletionAgent:
    """Create the Technical Architect agent"""
    return ChatCompletionAgent(
        kernel=kernel,
        name="Technical_Architect",
        instructions="""
You are a Technical Architect. Provide specific technology recommendations and implementation details.
Keep responses concise. End with "→ Documentation_Specialist should create final document."
""",
    )


def create_documentation_specialist(kernel: Kernel) -> ChatCompletionAgent:
    """Create the Documentation Specialist agent"""
    return ChatCompletionAgent(
        kernel=kernel,
        name="Documentation_Specialist",
        instructions="""
You are a Documentation Specialist. Create a concise architecture summary.
Include key decisions and implementation steps. End with "ARCHITECTURE DOCUMENT COMPLETE".
""",
    )


async def automated_demo():
    """Run an automated demo with a predefined requirement"""
    print("🏗️  Automated Architecture Squad Demo")
    print("=" * 50)

    # Create kernel and agents
    kernel = create_kernel()
    solution_architect = create_solution_architect(kernel)
    technical_architect = create_technical_architect(kernel)
    documentation_specialist = create_documentation_specialist(kernel)

    # Create simple group chat
    chat = AgentGroupChat(
        agents=[solution_architect, technical_architect,
                documentation_specialist]
    )

    print("✓ Architecture Squad initialized")

    # Test requirement
    requirement = """
Design a simple task management application that supports:
- User registration and authentication
- Creating, editing, and deleting tasks
- Task categorization and priority levels
- Basic task assignment to team members
- Expected users: ~1000 users, ~100 concurrent
"""

    print(f"\n📋 Requirement:\n{requirement}")
    print("\n" + "=" * 60)
    print("🤝 ARCHITECTURE SQUAD COLLABORATION")
    print("=" * 60)

    # Add user message
    await chat.add_chat_message(message=requirement)

    # Process through agents
    try:
        response_count = 0
        async for response in chat.invoke():
            if response:
                response_count += 1
                print(f"\n💭 {response.name} (Response {response_count}):")
                print("-" * 50)
                print(response.content)
                print("-" * 50)

                # Limit responses to prevent infinite loops
                if response_count >= 5 or "ARCHITECTURE DOCUMENT COMPLETE" in response.content:
                    print("\n✅ Architecture design completed!")
                    break

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(automated_demo())
