#!/usr/bin/env python3
"""
Test script for Documentation Specialist with MCP integration
"""

from agents.documentation_specialist import create_documentation_specialist_with_diagrams, create_enhanced_documentation_specialist
from utils.kernel import create_kernel
import asyncio
import os
import sys
from pathlib import Path

# Add the architecture-squad directory to the Python path
sys.path.append(str(Path(__file__).parent))


async def test_documentation_specialist_mcp():
    """Test the Documentation Specialist with MCP integration"""
    print("🧪 Testing Documentation Specialist with MCP Integration...")

    try:
        # Create kernel
        kernel = create_kernel()
        print("✅ Kernel created successfully")

        # Test creating the enhanced documentation specialist
        print("🔧 Creating enhanced documentation specialist with MCP integration...")
        agent = await create_enhanced_documentation_specialist(kernel)
        print(f"✅ Enhanced Documentation Specialist created: {agent.name}")

        # Test the MCP integration by checking if tools are available
        plugins = kernel.get_plugins()
        print(f"📋 Available plugins: {[plugin.name for plugin in plugins]}")

        # Check for the DiagramGenerator plugin
        diagram_plugin = None
        for plugin in plugins:
            if plugin.name == "DiagramGenerator":
                diagram_plugin = plugin
                break

        if diagram_plugin:
            print("✅ DiagramGenerator MCP plugin found and loaded!")
            functions = diagram_plugin.get_functions()
            print(
                f"🛠️  Available diagram generation functions: {[func.name for func in functions]}")
        else:
            print("❌ DiagramGenerator MCP plugin not found")
            return False

        print("🎉 Documentation Specialist MCP integration test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_fallback_documentation_specialist():
    """Test the fallback Documentation Specialist without MCP"""
    print("\n🧪 Testing fallback Documentation Specialist (without MCP)...")

    try:
        from agents.documentation_specialist import create_documentation_specialist

        kernel = create_kernel()
        agent = create_documentation_specialist(kernel)
        print(f"✅ Fallback Documentation Specialist created: {agent.name}")
        return True

    except Exception as e:
        print(f"❌ Fallback test failed with error: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Starting Documentation Specialist Integration Tests...\n")

    # Test MCP integration
    mcp_success = await test_documentation_specialist_mcp()

    # Test fallback
    fallback_success = await test_fallback_documentation_specialist()

    print(f"\n📊 Test Results:")
    print(f"   MCP Integration: {'✅ PASS' if mcp_success else '❌ FAIL'}")
    print(f"   Fallback Agent:  {'✅ PASS' if fallback_success else '❌ FAIL'}")

    if mcp_success and fallback_success:
        print("\n🎉 All tests passed! Documentation Specialist MCP integration is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
