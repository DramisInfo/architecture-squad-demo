#!/usr/bin/env python3
"""
Quick validation script to test imports and agent creation
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")

    try:
        # Test agent imports
        from agents import (
            create_platform_selector,
            create_solution_architect,
            create_azure_solution_architect,
            create_aws_solution_architect,
            create_kubernetes_solution_architect,
            create_technical_architect,
            create_security_architect,
            create_data_architect,
            create_documentation_specialist,
        )
        print("✅ All agent imports successful")

        # Test utility imports
        from utils import create_kernel, create_architecture_group_chat
        print("✅ Utility imports successful")

        # Test strategy imports
        from strategies import create_selection_function, create_termination_function
        print("✅ Strategy imports successful")

        # Test kernel creation
        kernel = create_kernel()
        print("✅ Kernel creation successful")

        # Test agent creation
        platform_selector = create_platform_selector(kernel)
        azure_architect = create_azure_solution_architect(kernel)
        aws_architect = create_aws_solution_architect(kernel)
        k8s_architect = create_kubernetes_solution_architect(kernel)
        print("✅ Certified solution architects created successfully")

        # Test chat creation
        chat = create_architecture_group_chat(kernel)
        print("✅ Architecture group chat created successfully")

        print("\n🎉 All validations passed! The improved Architecture Squad is ready.")
        return True

    except Exception as e:
        print(f"❌ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_imports()
    if not success:
        sys.exit(1)
    print("\nThe Architecture Squad now includes:")
    print("• Platform Selector - Routes to appropriate cloud platform specialist")
    print("• Azure Solution Architect - Microsoft Azure certified solutions")
    print("• AWS Solution Architect - Amazon Web Services certified solutions")
    print("• Kubernetes Solution Architect - Container orchestration & OpenShift solutions")
    print("• General Solution Architect - Platform-agnostic solutions")
    print("• Technical, Security, Data Architects and Documentation Specialist")
