#!/usr/bin/env python3
"""
Test Azure AI Agents functionality in the new Semantic Kernel
"""

import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Try to import Azure AI Agents
try:
    from azure.ai.agents import AgentsClient
    print("✓ Azure AI Agents available")
    AZURE_AGENTS_AVAILABLE = True
except ImportError:
    print("✗ Azure AI Agents not available")
    AZURE_AGENTS_AVAILABLE = False

# Try to import AgentGroupChat from semantic_kernel
try:
    from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
    print("✓ Semantic Kernel AgentGroupChat available")
    SK_AGENTS_AVAILABLE = True
except ImportError:
    print("✗ Semantic Kernel AgentGroupChat not available")
    SK_AGENTS_AVAILABLE = False


async def test_available_approaches():
    """Test what agent approaches are available"""
    load_dotenv()

    # Create basic kernel
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

    print("\n=== Testing Agent Approaches ===")

    # Test Semantic Kernel Agents
    if SK_AGENTS_AVAILABLE:
        try:
            agent = ChatCompletionAgent(
                kernel=kernel,
                name="Test_Agent",
                instructions="You are a test agent.",
            )
            print("✓ ChatCompletionAgent created successfully")

            # Try to create AgentGroupChat
            try:
                chat = AgentGroupChat(agents=[agent])
                print("✓ AgentGroupChat created successfully")
            except Exception as e:
                print(f"✗ AgentGroupChat failed: {e}")

        except Exception as e:
            print(f"✗ ChatCompletionAgent failed: {e}")

    # Test Azure AI Agents
    if AZURE_AGENTS_AVAILABLE:
        try:
            # This would require Azure AI Studio setup
            print("Azure AI Agents is available but requires Azure AI Studio setup")
        except Exception as e:
            print(f"✗ Azure AI Agents test failed: {e}")

    print("\n=== Recommendations ===")
    if SK_AGENTS_AVAILABLE:
        print("✓ Use Semantic Kernel AgentGroupChat approach")
    elif AZURE_AGENTS_AVAILABLE:
        print("✓ Use Azure AI Agents approach (requires Azure AI Studio)")
    else:
        print("✓ Use basic chat completion with manual agent coordination")

if __name__ == "__main__":
    asyncio.run(test_available_approaches())
