#!/usr/bin/env python3
"""
Test script to demonstrate Azure architect with research capabilities
"""

from agents.azure_solution_architect import create_azure_solution_architect
from utils.kernel import create_kernel
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_azure_architect_research():
    """Test the Azure architect with research capabilities"""

    print("🔄 Initializing Azure Solution Architect with Research Capabilities...")

    # Create kernel
    kernel = create_kernel()

    # Create Azure architect agent
    azure_architect = create_azure_solution_architect(kernel)

    print("✅ Azure architect initialized successfully!")
    print("🔍 Available research functions:")

    # List available functions
    if hasattr(azure_architect.kernel.plugins, 'azure_research'):
        print("   - research_azure_topic")
        print("   - get_azure_service_info")
    else:
        print("   - Research functions may not be loaded (check MCP server)")

    # Test scenario: E-commerce platform architecture
    test_scenario = """
    Design a scalable e-commerce platform architecture for Azure that needs to handle:
    - High traffic during sales events (Black Friday, etc.)
    - Global customer base with low latency requirements
    - PCI DSS compliance for payment processing
    - Real-time inventory management
    - Integration with third-party logistics providers
    """

    print(f"\n📋 Test Scenario:")
    print(test_scenario)
    print("\n" + "="*80)
    print("🏗️ Azure Architect Response:")
    print("="*80)

    try:
        # Create a simple chat to test the agent
        from semantic_kernel.agents import AgentGroupChat
        from semantic_kernel.contents import ChatMessageContent, AuthorRole

        # Create a simple group chat with just the Azure architect
        chat = AgentGroupChat(agents=[azure_architect])

        # Add the scenario as a user message
        user_message = ChatMessageContent(
            role=AuthorRole.USER,
            content=f"User requirements: {test_scenario}"
        )

        # Add message to chat and get response
        await chat.add_chat_message(user_message)

        print("Processing request with Azure architect...")

        # Get the architect's response
        async for response in chat.invoke():
            if response.content:
                print(f"\n💡 {response.name}:")
                print("-" * 60)
                print(response.content)
                print("-" * 60)
                break

    except Exception as e:
        print(f"❌ Error during architect invocation: {e}")
        print("This might be due to missing API keys, network issues, or API changes.")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)
    print("✅ Test completed!")


if __name__ == "__main__":
    asyncio.run(test_azure_architect_research())
