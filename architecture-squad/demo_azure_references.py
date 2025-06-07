#!/usr/bin/env python3
"""
Simple demonstration of Azure architect with reference architectures
"""

from agents.azure_solution_architect import create_azure_solution_architect
from utils.kernel import create_kernel
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


async def demo_azure_architect_with_references():
    """Demonstrate Azure architect providing reference architectures"""

    print("🚀 Azure Architect Reference Architecture Demo")
    print("=" * 80)

    # Create kernel and Azure architect
    kernel = create_kernel()
    azure_architect = create_azure_solution_architect(kernel)

    # Simple test scenario
    scenario = "Design an Azure microservices architecture for a retail application"

    print(f"📋 Scenario: {scenario}")
    print("\n" + "=" * 80)
    print("🎯 Azure Architect Response:")
    print("=" * 80)

    try:
        async for response in azure_architect.invoke(scenario):
            if response.content:
                print(response.content)

                # Count reference architecture links
                content = response.content
                link_count = content.count("https://learn.microsoft.com")
                ref_arch_mentions = content.lower().count("reference architecture")

                print("\n" + "=" * 80)
                print(
                    f"✅ SUCCESS: Found {link_count} Azure documentation links")
                print(
                    f"✅ SUCCESS: Found {ref_arch_mentions} reference architecture mentions")
                break

    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n🎯 Demo completed!")


if __name__ == "__main__":
    asyncio.run(demo_azure_architect_with_references())
