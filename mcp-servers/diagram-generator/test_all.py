#!/usr/bin/env python3
"""
Master test runner for the Diagram Generator MCP server.

This file provides a unified entry point for running all tests in the project.
It can run tests individually or as a complete suite.

Usage:
    python test_all.py              # Run all tests
    python test_all.py --fast       # Run basic tests only
    python test_all.py --verbose    # Run with detailed output
    python test_all.py --component  # Run component tests only
    python test_all.py --integration # Run integration tests only
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import all test modules
from tests.test_server_initialization import TestServerInitialization
from tests.test_component_listing import TestComponentListing
from tests.test_simple_diagrams import TestSimpleDiagrams
from tests.test_clustered_diagrams import TestClusteredDiagrams
from tests.test_aws_diagrams import TestAWSDiagrams
from tests.test_kubernetes_diagrams import TestKubernetesDiagrams
from tests.test_microservices_diagrams import TestMicroservicesDiagrams
from tests.test_error_handling import TestErrorHandling
from tests.test_tool_validation import TestToolValidation


class DiagramGeneratorTestSuite:
    """Master test suite for the Diagram Generator MCP server."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    async def run_test_class(self, test_class, class_name: str):
        """Run all tests in a test class."""
        self.log(f"\n🧪 Running {class_name}...")
        
        instance = test_class()
        test_methods = [method for method in dir(instance) if method.startswith('test_')]
        
        for method_name in test_methods:
            try:
                self.log(f"  ⏳ {method_name}...")
                test_method = getattr(instance, method_name)
                await test_method()
                self.log(f"  ✅ {method_name}")
                self.passed += 1
            except Exception as e:
                self.log(f"  ❌ {method_name}: {str(e)}")
                self.failed += 1
                self.errors.append(f"{class_name}.{method_name}: {str(e)}")
    
    async def run_basic_tests(self):
        """Run basic functionality tests."""
        print("🚀 Running basic tests...")
        
        await self.run_test_class(TestServerInitialization, "TestServerInitialization")
        await self.run_test_class(TestComponentListing, "TestComponentListing")
        await self.run_test_class(TestSimpleDiagrams, "TestSimpleDiagrams")
    
    async def run_component_tests(self):
        """Run component-specific tests."""
        print("🔧 Running component tests...")
        
        await self.run_test_class(TestSimpleDiagrams, "TestSimpleDiagrams")
        await self.run_test_class(TestClusteredDiagrams, "TestClusteredDiagrams")
        await self.run_test_class(TestAWSDiagrams, "TestAWSDiagrams")
        await self.run_test_class(TestKubernetesDiagrams, "TestKubernetesDiagrams")
        await self.run_test_class(TestMicroservicesDiagrams, "TestMicroservicesDiagrams")
    
    async def run_integration_tests(self):
        """Run integration and validation tests."""
        print("🔗 Running integration tests...")
        
        await self.run_test_class(TestErrorHandling, "TestErrorHandling")
        await self.run_test_class(TestToolValidation, "TestToolValidation")
    
    async def run_all_tests(self):
        """Run the complete test suite."""
        print("🎯 Running complete test suite...")
        
        await self.run_test_class(TestServerInitialization, "TestServerInitialization")
        await self.run_test_class(TestComponentListing, "TestComponentListing")
        await self.run_test_class(TestSimpleDiagrams, "TestSimpleDiagrams")
        await self.run_test_class(TestClusteredDiagrams, "TestClusteredDiagrams")
        await self.run_test_class(TestAWSDiagrams, "TestAWSDiagrams")
        await self.run_test_class(TestKubernetesDiagrams, "TestKubernetesDiagrams")
        await self.run_test_class(TestMicroservicesDiagrams, "TestMicroservicesDiagrams")
        await self.run_test_class(TestErrorHandling, "TestErrorHandling")
        await self.run_test_class(TestToolValidation, "TestToolValidation")
    
    def print_summary(self):
        """Print test execution summary."""
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{'='*60}")
        print(f"📊 TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.errors:
            print(f"\n❌ FAILED TESTS:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.failed == 0:
            print(f"\n🎉 All tests passed! The Diagram Generator MCP server is working correctly.")
        else:
            print(f"\n⚠️  Some tests failed. Please review the errors above.")
        
        print(f"{'='*60}")


async def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Diagram Generator MCP Server Test Suite")
    parser.add_argument("--fast", action="store_true", help="Run basic tests only")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--component", action="store_true", help="Run component tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    
    args = parser.parse_args()
    
    # Create test suite
    suite = DiagramGeneratorTestSuite(verbose=args.verbose)
    
    try:
        if args.fast:
            await suite.run_basic_tests()
        elif args.component:
            await suite.run_component_tests()
        elif args.integration:
            await suite.run_integration_tests()
        else:
            await suite.run_all_tests()
            
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        return 1
    finally:
        suite.print_summary()
    
    # Return exit code based on test results
    return 0 if suite.failed == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
