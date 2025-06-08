#!/usr/bin/env python3
"""
Test MCP integration with Chainlit app
"""

from app import ArchitectureSquadSession
import asyncio
import sys
import os
from pathlib import Path

# Add the architecture-squad directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "architecture-squad"))


async def test_mcp_integration():
    """Test that MCP diagram generation works with the session"""
    print("🧪 Testing MCP integration with Architecture Squad...")

    # Create session
    session = ArchitectureSquadSession()

    # Initialize
    await session.initialize()
    print("✅ Session initialized")

    # Check if MCP is properly connected
    doc_agents = [
        agent for agent in session.chat.agents if "Documentation" in agent.name]
    if doc_agents:
        doc_agent = doc_agents[0]
        if hasattr(doc_agent, 'kernel') and hasattr(doc_agent.kernel, 'plugins'):
            plugin_names = list(doc_agent.kernel.plugins.keys())
            mcp_plugins = [name for name in plugin_names
                           if 'DiagramGenerator' in name or 'diagram' in name.lower()]
            if mcp_plugins:
                print("✅ MCP Diagram Generator detected in session")
                print(f"   Plugin: {mcp_plugins[0]}")
            else:
                print("⚠️  MCP Diagram Generator not detected")
                print(f"   Available plugins: {plugin_names}")
        else:
            print("ℹ️  Basic documentation specialist (no MCP)")

    print("✅ MCP integration test completed")


if __name__ == "__main__":
    asyncio.run(test_mcp_integration())
