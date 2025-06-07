#!/usr/bin/env python3
"""
Simple working demo of the architecture squad without API calls
"""

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_simple_kernel():
    """Create a simple kernel without API services for testing"""
    return Kernel()


def create_test_agents(kernel):
    """Create test agents without actual AI services"""

    solution_architect = ChatCompletionAgent(
        kernel=kernel,
        name="Solution_Architect",
        instructions="You are a Solution Architect.",
    )

    technical_architect = ChatCompletionAgent(
        kernel=kernel,
        name="Technical_Architect",
        instructions="You are a Technical Architect.",
    )

    return [solution_architect, technical_architect]


def main():
    """Simple test of agent creation"""
    print("Simple Architecture Squad Test")
    print("=" * 40)

    try:
        # Create kernel
        kernel = create_simple_kernel()
        print("✓ Kernel created")

        # Create agents
        agents = create_test_agents(kernel)
        print(f"✓ {len(agents)} agents created")

        for agent in agents:
            print(f"  - {agent.name}")

        print("\n✓ Basic setup is working!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
