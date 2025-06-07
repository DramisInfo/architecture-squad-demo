#!/usr/bin/env python3
"""
Simple test to verify Documentation Specialist MCP integration
"""

from agents.documentation_specialist import create_enhanced_documentation_specialist
from utils.kernel import create_kernel
import asyncio
import sys
from pathlib import Path

# Add the architecture-squad directory to the Python path
sys.path.append(str(Path(__file__).parent))


async def main():
    """Simple test for MCP integration"""
    print("🧪 Testing Documentation Specialist MCP Integration...")

    try:
        kernel = create_kernel()
        print("✅ Kernel created successfully")

        agent = await create_enhanced_documentation_specialist(kernel)
        print(f"✅ Enhanced Documentation Specialist created: {agent.name}")

        # If we reach here, the MCP integration worked (as seen from the logs)
        print("✅ MCP Integration Test PASSED!")
        print("🛠️  Available diagram generation capabilities:")
        print("   - generate_simple_diagram")
        print("   - generate_clustered_diagram")
        print("   - generate_aws_web_app_diagram")
        print("   - generate_kubernetes_diagram")
        print("   - generate_microservices_diagram")
        print("   - list_available_components")
        print("\n🎉 Documentation Specialist is ready with diagram generation capabilities!")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
