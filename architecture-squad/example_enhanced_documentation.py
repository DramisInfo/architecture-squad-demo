#!/usr/bin/env python3
"""
Usage example for the Enhanced Documentation Specialist with MCP integration

This example shows how to use the documentation specialist with diagram generation
capabilities in the architecture squad workflow.
"""

from agents.documentation_specialist import create_enhanced_documentation_specialist
from utils.kernel import create_kernel
import asyncio
import sys
from pathlib import Path

# Add the architecture-squad directory to the Python path
sys.path.append(str(Path(__file__).parent))


async def example_usage():
    """Example of using the enhanced documentation specialist"""
    print("🚀 Enhanced Documentation Specialist Usage Example")
    print("=" * 60)

    # Create kernel and enhanced agent
    kernel = create_kernel()
    doc_specialist = await create_enhanced_documentation_specialist(kernel)

    print(f"✅ Created agent: {doc_specialist.name}")
    print("🎯 Agent Instructions Summary:")
    print("   - Comprehensive technical documentation creation")
    print("   - Visual architecture diagram generation")
    print("   - Integration of all architectural perspectives")
    print("   - Professional technical writing")
    print("   - Reference preservation and organization")

    print("\n📋 Available Diagram Generation Tools:")
    diagram_tools = [
        "generate_simple_diagram - Basic architecture diagrams with components and connections",
        "generate_clustered_diagram - Diagrams with grouped components (tiers, environments)",
        "generate_aws_web_app_diagram - AWS-specific web application architectures",
        "generate_kubernetes_diagram - Kubernetes cluster architecture diagrams",
        "generate_microservices_diagram - Microservices architecture diagrams",
        "list_available_components - List all available diagram components across providers"
    ]

    for i, tool in enumerate(diagram_tools, 1):
        print(f"   {i}. {tool}")

    print("\n🏗️ Integration in Architecture Squad:")
    print("   To use this enhanced agent in your architecture squad workflow:")
    print("   1. Replace create_documentation_specialist() calls with:")
    print("      await create_enhanced_documentation_specialist(kernel)")
    print("   2. The agent will automatically generate diagrams when processing")
    print("      architectural inputs from other squad members")
    print("   3. Diagrams will be embedded in the final documentation")

    print("\n📖 Example Agent Workflow:")
    print("   1. Receives inputs from Solution, Technical, Security, and Data Architects")
    print("   2. Analyzes architecture type (web app, microservices, k8s, etc.)")
    print("   3. Generates appropriate diagrams using MCP tools")
    print("   4. Creates comprehensive documentation with visual aids")
    print("   5. Includes all references and links from architectural team")
    print("   6. Provides complete technical documentation with diagrams")

    print("\n✨ Benefits of MCP Integration:")
    print("   ✅ Automated visual diagram generation")
    print("   ✅ Support for multiple cloud providers (AWS, Azure, GCP)")
    print("   ✅ Kubernetes and on-premises components")
    print("   ✅ Professional architecture visualization")
    print("   ✅ Consistent diagram styling and formatting")
    print("   ✅ Integration with existing documentation workflow")

    print("\n🎉 The Enhanced Documentation Specialist is ready for use!")
    print("   Use create_enhanced_documentation_specialist() in your squad workflows")


if __name__ == "__main__":
    asyncio.run(example_usage())
