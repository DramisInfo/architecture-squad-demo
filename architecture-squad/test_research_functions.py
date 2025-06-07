#!/usr/bin/env python3
"""
Quick integration test to verify Azure research functions work directly
"""

from agents.azure_solution_architect import AzureResearchPlugin
from utils.kernel import create_kernel
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_research_functions():
    """Test the research functions directly"""

    print("🧪 Testing Azure Research Functions Directly")
    print("=" * 50)

    # Create the research plugin
    plugin = AzureResearchPlugin()

    # Test 1: Research a topic
    print("1️⃣ Testing research_azure_topic...")
    topic_result = await plugin.research_azure_topic("Azure App Service scaling")
    print(f"Result: {topic_result[:200]}..." if len(
        topic_result) > 200 else topic_result)
    print()

    # Test 2: Get service info
    print("2️⃣ Testing get_azure_service_info...")
    service_result = await plugin.get_azure_service_info("Functions")
    print(f"Result: {service_result[:200]}..." if len(
        service_result) > 200 else service_result)
    print()

    # Test 3: Test with kernel integration
    print("3️⃣ Testing kernel integration...")
    kernel = create_kernel()

    try:
        kernel.add_plugin(plugin, plugin_name="azure_research")
        print("✅ Plugin added to kernel successfully")

        # List functions
        functions = kernel.plugins["azure_research"]
        print(f"Available functions: {list(functions.keys())}")

    except Exception as e:
        print(f"❌ Error adding plugin to kernel: {e}")

    print("\n🎉 Research function tests completed!")


if __name__ == "__main__":
    asyncio.run(test_research_functions())
