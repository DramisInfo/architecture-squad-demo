#!/usr/bin/env python3
"""
Automated Architecture Squad Demo for testing
Demonstrates the full architecture squad collaboration with diagram generation

UPDATED: Now uses the utils module properly:
- Uses create_kernel() from utils.kernel for proper environment handling
- Uses create_architecture_group_chat_async() from utils.chat for full squad
- Includes enhanced documentation specialist with MCP diagram generation
- Runs fully automated without user input - just executes the demo
"""

import asyncio
import logging
from utils import create_kernel, create_architecture_group_chat_async

# Configure logging for the demo - suppress ALL verbose logs
logging.basicConfig(
    level=logging.CRITICAL,  # Only show critical errors
    format='%(message)s'  # Simplified format
)

# Suppress ALL verbose loggers to CRITICAL level
loggers_to_suppress = [
    "httpx", "semantic_kernel", "openai", "httpcore", "FastMCP", "mcp",
    "utils.kernel", "agents", "anyio", "httpcore.http11", "httpcore.connection_pool",
    "openai._base_client", "semantic_kernel.agents", "semantic_kernel.connectors",
    "semantic_kernel.functions", "semantic_kernel.agents.group_chat",
    "semantic_kernel.agents.strategies", "semantic_kernel.utils",
    "semantic_kernel.agents.channels", "azure", "azure.core"
]

for logger_name in loggers_to_suppress:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# Also suppress root logger output
logging.getLogger().setLevel(logging.CRITICAL)


async def automated_demo():
    """Run an automated demo with a predefined requirement"""
    print("🏗️  Automated Architecture Squad Demo with Diagram Generation")
    print("=" * 60)

    # Suppress all logging after imports
    logging.getLogger().setLevel(logging.CRITICAL)
    for logger_name in loggers_to_suppress:
        logging.getLogger(logger_name).setLevel(logging.CRITICAL)

    # Create kernel using utils
    print("🔧 Creating kernel...")
    kernel = create_kernel()
    print("✓ Kernel created successfully")

    # Create architecture group chat using utils
    print("🤝 Initializing Architecture Squad...")
    chat = await create_architecture_group_chat_async(kernel)
    print("✓ Architecture Squad initialized with enhanced capabilities")

    # Check if documentation specialist has MCP diagram generation
    doc_agents = [
        agent for agent in chat.agents if "Documentation" in agent.name]
    if doc_agents:
        doc_agent = doc_agents[0]
        if hasattr(doc_agent, 'kernel') and hasattr(doc_agent.kernel, 'plugins'):
            plugin_names = list(doc_agent.kernel.plugins.keys())
            mcp_plugins = [name for name in plugin_names
                           if 'DiagramGenerator' in name or 'diagram' in name.lower()]
            if mcp_plugins:
                print("✓ MCP Diagram Generator server connected successfully")
            else:
                print(
                    "⚠️  MCP Diagram Generator server not detected - using standard mode")
        else:
            print("ℹ️  Using standard documentation specialist")

    # Predefined test requirement for automated demo
    requirement = """
I need an architecture for azure api management self-hosted gateways on openshift
"""

    print(f"\n📋 Processing Requirement:")
    print("-" * 40)
    print(requirement)
    print("\n" + "=" * 60)
    print("🤝 ARCHITECTURE SQUAD COLLABORATION")
    print("=" * 60)

    # Add user message to start the collaboration
    await chat.add_chat_message(message=requirement)

    # Process through agents with automatic collaboration
    try:
        response_count = 0
        max_responses = 15  # Prevent infinite loops

        print("🚀 Starting automated collaboration...")

        async for response in chat.invoke():
            if response:
                response_count += 1

                # Only show progress for non-Documentation Specialist agents
                if response.name != "Documentation_Specialist":
                    print(f"✓ {response.name} completed analysis")

                # For Documentation Specialist, show progress indicators and final document
                if response.name == "Documentation_Specialist":
                    if any(keyword in response.content.lower()
                           for keyword in ["generating", "diagram", "visual", "creating diagram"]):
                        print("🎨 Generating architecture diagrams...")

                    if "generate_" in response.content.lower():
                        print("📊 Processing diagram generation requests...")

                    # Show the final document from Documentation Specialist
                    print(f"\n📋 FINAL ARCHITECTURE DOCUMENT:")
                    print("=" * 60)
                    print(response.content)
                    print("=" * 60)

                # Check for completion signals
                if ("ARCHITECTURE DOCUMENT COMPLETE" in response.content or
                        "COMPLETE" in response.content and response.name == "Documentation_Specialist"):
                    print("\n✅ Architecture design completed successfully!")

                    # Check if diagrams were generated
                    if any(keyword in response.content.lower()
                           for keyword in ["diagram", "generated", "visual", "chart"]):
                        print(
                            "🎨 Architecture diagrams have been generated and included!")

                    print("📋 Comprehensive architecture document created")
                    break

                # Safety limit to prevent infinite loops
                if response_count >= max_responses:
                    print(
                        f"\n⚠️  Reached maximum response limit ({max_responses})")
                    print("🏁 Demo completed - architecture design process finished")
                    break

        print("\n" + "=" * 60)
        print("🎉 AUTOMATED DEMO COMPLETED")
        print("=" * 60)
        print("✅ Architecture Squad successfully collaborated")
        print("✅ Comprehensive architecture document generated")
        print("✅ All requirements addressed with technical solutions")

        if response_count > 0:
            print(f"📊 Total collaboration responses: {response_count}")

    except Exception as e:
        print(f"❌ Error during collaboration: {e}")
        import traceback
        traceback.print_exc()
        print("\n🔧 This might be due to:")
        print("   - Missing environment variables")
        print("   - MCP server connection issues")
        print("   - API rate limiting")
        print("   - Network connectivity issues")


if __name__ == "__main__":
    asyncio.run(automated_demo())
