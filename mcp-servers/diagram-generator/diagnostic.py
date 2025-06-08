#!/usr/bin/env python3
"""
Diagnostic test to check available components
"""

import asyncio
from server import list_available_components


async def diagnostic():
    """Check what components are available"""
    print("🔍 Checking available components...")

    result = list_available_components()

    if result["success"]:
        print("✅ Successfully retrieved available components")
        components = result["components"]

        print(f"\n📊 Available providers: {list(components.keys())}")

        for provider in list(components.keys())[:3]:  # Show first 3 providers
            print(f"\n🔧 {provider.upper()} categories:")
            categories = list(components[provider].keys())
            for category in categories[:3]:  # Show first 3 categories
                sample_components = list(components[provider][category])[
                    :3]  # Show first 3 components
                print(f"   - {category}: {sample_components}")
    else:
        print(
            f"❌ Failed to retrieve components: {result.get('error', 'Unknown error')}")

    return result


if __name__ == "__main__":
    asyncio.run(diagnostic())
