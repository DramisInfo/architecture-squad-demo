#!/usr/bin/env python3
"""
Pytest runner for the Diagram Generator MCP server.

This file provides a unified entry point for running all tests using pytest.
It replaces the custom test runner with standard pytest functionality.

Usage:
    python test_all.py              # Run all tests
    python test_all.py --fast       # Run basic tests only  
    python test_all.py --verbose    # Run with detailed output
    python test_all.py --component  # Run component tests only
    python test_all.py --integration # Run integration tests only
    
Or use pytest directly:
    pytest                          # Run all tests
    pytest -v                       # Verbose output
    pytest tests/test_simple_diagrams.py  # Run specific test file
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_pytest_with_args(pytest_args):
    """Run pytest with the specified arguments."""
    # Add the current directory to Python path
    current_dir = str(Path(__file__).parent)

    # Build the pytest command
    cmd = [sys.executable, "-m", "pytest"] + pytest_args

    print(f"Running: {' '.join(cmd)}")
    print(f"Working directory: {current_dir}")
    print("-" * 60)

    # Run pytest
    result = subprocess.run(cmd, cwd=current_dir)
    return result.returncode


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description="Diagram Generator MCP Server Test Suite")
    parser.add_argument("--fast", action="store_true",
                        help="Run basic tests only")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--component", action="store_true",
                        help="Run component tests only")
    parser.add_argument("--integration", action="store_true",
                        help="Run integration tests only")

    args = parser.parse_args()

    # Build pytest arguments
    pytest_args = []

    if args.verbose:
        pytest_args.extend(["-v", "-s"])

    # Select test categories
    if args.fast:
        # Basic tests
        pytest_args.extend([
            "tests/test_server_initialization.py",
            "tests/test_component_listing.py",
            "tests/test_simple_diagrams.py"
        ])
    elif args.component:
        # Component tests
        pytest_args.extend([
            "tests/test_simple_diagrams.py",
            "tests/test_clustered_diagrams.py",
            "tests/test_aws_diagrams.py",
            "tests/test_kubernetes_diagrams.py",
            "tests/test_microservices_diagrams.py"
        ])
    elif args.integration:
        # Integration tests
        pytest_args.extend([
            "tests/test_error_handling.py",
            "tests/test_tool_validation.py"
        ])
    else:
        # All tests
        pytest_args.append("tests/")

    # Add common pytest options
    pytest_args.extend([
        "--tb=short",  # Shorter traceback format
        "--strict-markers",  # Require marker registration
        "--disable-warnings",  # Disable warnings for cleaner output
        "-k", "not trio"  # Skip tests that require trio library
    ])

    try:
        exit_code = run_pytest_with_args(pytest_args)

        if exit_code == 0:
            print(
                "\n🎉 All tests passed! The Diagram Generator MCP server is working correctly.")
        else:
            print(
                f"\n⚠️  Some tests failed (exit code: {exit_code}). Please review the output above.")

        return exit_code

    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
