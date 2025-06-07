#!/usr/bin/env python3
"""
Test Azure Solution Architect with Reference Architecture Integration
"""

from agents.azure_solution_architect import create_azure_solution_architect
from utils.kernel import create_kernel
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


async def test_azure_architect_with_reference_architectures():
    """Test Azure architect's ability to find and include reference architectures"""

    print("🧪 Testing Azure Solution Architect with Reference Architecture Integration...")
    print("=" * 80)

    # Create kernel and Azure architect
    kernel = create_kernel()
    azure_architect = create_azure_solution_architect(kernel)

    # Test scenario: E-commerce platform
    test_scenario = """
    Design an Azure architecture for a modern e-commerce platform with the following requirements:
    - High availability and scalability
    - Global reach with low latency
    - Secure payment processing
    - Real-time inventory management
    - Analytics and reporting capabilities
    
    Please include relevant Azure reference architectures in your recommendation.
    """

    print("📋 Test Scenario:")
    print(test_scenario)
    print("\n" + "=" * 80)
    print("🏗️ Azure Architect Response with Reference Architectures:")
    print("=" * 80)

    try:
        # Get response from Azure architect
        async for response in azure_architect.invoke(test_scenario):
            if response.content:
                print(f"\n{response.content}")

                # Check if response includes reference architectures
                content_lower = response.content.lower()
                has_reference_arch = any(keyword in content_lower for keyword in [
                    'reference architecture', 'architecture center', 'learn.microsoft.com',
                    'reference pattern', 'solution pattern', '🔗', '📋', '🏗️'
                ])

                if has_reference_arch:
                    print("\n" + "=" * 80)
                    print("✅ SUCCESS: Response includes reference architecture links!")
                else:
                    print("\n" + "=" * 80)
                    print(
                        "❌ WARNING: Response may not include reference architecture links")

                break

    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        return False

    print("\n" + "=" * 80)
    print("🎯 Test completed successfully!")
    return True


async def test_reference_architecture_function():
    """Test the reference architecture function directly"""

    print("\n🔍 Testing Reference Architecture Function Directly...")
    print("=" * 80)

    # Create kernel and get the research plugin
    kernel = create_kernel()
    azure_architect = create_azure_solution_architect(kernel)

    # Test the reference architecture function
    try:
        # Get the plugin from the kernel
        plugin = kernel.plugins.get("azure_research")
        if plugin:
            ref_arch_function = plugin.get(
                "find_azure_reference_architectures")
            if ref_arch_function:
                # Test searching for e-commerce reference architectures
                result = await ref_arch_function.invoke(kernel, use_case="e-commerce microservices")
                print("🏛️ Reference Architecture Search Results:")
                print(result.value)

                # Check if results contain links
                if "http" in str(result.value) or "🔗" in str(result.value):
                    print(
                        "\n✅ SUCCESS: Reference architecture function returned links!")
                else:
                    print(
                        "\n⚠️ INFO: Reference architecture function returned information but may not have found specific links")
            else:
                print("❌ Reference architecture function not found in plugin")
        else:
            print("❌ Azure research plugin not found in kernel")

    except Exception as e:
        print(f"❌ Error testing reference architecture function: {e}")


if __name__ == "__main__":
    print("🚀 Starting Azure Reference Architecture Integration Tests")
    print("=" * 80)

    async def run_all_tests():
        await test_reference_architecture_function()
        await test_azure_architect_with_reference_architectures()

    asyncio.run(run_all_tests())
