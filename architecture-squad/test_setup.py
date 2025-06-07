#!/usr/bin/env python3
"""
Test script to validate the architecture squad setup without making API calls
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test all the module imports"""
    try:
        print("Testing imports...")

        # Test utils imports
        from utils import create_kernel, create_architecture_group_chat
        print("✓ Utils imports successful")

        # Test agent imports
        from agents import (
            create_solution_architect,
            create_technical_architect,
            create_security_architect,
            create_data_architect,
            create_documentation_specialist,
        )
        print("✓ Agent imports successful")

        # Test strategy imports
        from strategies import create_selection_function, create_termination_function
        print("✓ Strategy imports successful")

        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False


def test_object_creation():
    """Test creating kernel and chat objects"""
    try:
        print("\nTesting object creation...")

        from utils import create_kernel, create_architecture_group_chat

        # Create kernel
        kernel = create_kernel()
        print("✓ Kernel created successfully")

        # Create chat
        chat = create_architecture_group_chat(kernel)
        print(f"✓ Chat created successfully with {len(chat.agents)} agents")

        # List agent names
        agent_names = [agent.name for agent in chat.agents]
        print(f"✓ Agents: {', '.join(agent_names)}")

        return True
    except Exception as e:
        print(f"✗ Object creation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("Architecture Squad Test Suite")
    print("=" * 50)

    all_passed = True

    # Test imports
    all_passed &= test_imports()

    # Test object creation
    all_passed &= test_object_creation()

    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed!")
        print("The architecture squad is ready to use.")
    else:
        print("✗ Some tests failed!")
        print("Please fix the issues before running the demo.")
        sys.exit(1)


if __name__ == "__main__":
    main()
