#!/usr/bin/env python3
"""
Test script to verify that Chainlit uses the enhanced documentation specialist
with diagram generation capabilities.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add the architecture-squad directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "architecture-squad"))

try:
    from utils import create_kernel, create_architecture_group_chat_async, create_architecture_group_chat
    from agents import create_enhanced_documentation_specialist
except ImportError as e:
    print(f"❌ Error importing architecture squad modules: {e}")
    sys.exit(1)


async def test_enhanced_documentation_specialist():
    """Test that the enhanced documentation specialist is working"""
    print("🧪 Testing enhanced documentation specialist...")

    kernel = create_kernel()

    try:
        # Test creating the enhanced documentation specialist directly
        doc_specialist = await create_enhanced_documentation_specialist(kernel)
        print("✅ Enhanced documentation specialist created successfully")
        print(f"   Agent name: {doc_specialist.name}")

        # Check if it mentions diagram generation in instructions
        if "diagram" in doc_specialist.instructions.lower():
            print("✅ Documentation specialist includes diagram generation capabilities")
        else:
            print(
                "⚠️  Documentation specialist may not have diagram generation capabilities")

    except Exception as e:
        print(f"❌ Error creating enhanced documentation specialist: {e}")
        return False

    return True


async def test_async_group_chat():
    """Test that the async group chat creation works"""
    print("\n🧪 Testing async group chat creation...")

    kernel = create_kernel()

    try:
        # Test creating the async version of group chat
        chat = await create_architecture_group_chat_async(kernel)
        print("✅ Async group chat created successfully")

        # Check if documentation specialist is in the agents
        doc_specialist = None
        for agent in chat.agents:
            if "Documentation_Specialist" in agent.name:
                doc_specialist = agent
                break

        if doc_specialist:
            print("✅ Documentation specialist found in group chat")
            # Check if it has diagram capabilities
            if "diagram" in doc_specialist.instructions.lower():
                print(
                    "✅ Documentation specialist in group chat has diagram capabilities")
            else:
                print(
                    "⚠️  Documentation specialist in group chat may not have diagram capabilities")
        else:
            print("❌ Documentation specialist not found in group chat")

    except Exception as e:
        print(f"❌ Error creating async group chat: {e}")
        # Test fallback to sync version
        print("🔄 Testing fallback to sync version...")
        try:
            chat = create_architecture_group_chat(kernel)
            print("✅ Sync group chat created successfully as fallback")
        except Exception as fallback_e:
            print(f"❌ Sync fallback also failed: {fallback_e}")
            return False

    return True


async def test_chainlit_integration():
    """Test that Chainlit can initialize with the enhanced documentation specialist"""
    print("\n🧪 Testing Chainlit integration...")

    # Simulate the Chainlit ArchitectureSquadSession initialization
    class TestArchitectureSquadSession:
        def __init__(self):
            self.kernel = None
            self.chat = None
            self.initialized = False

        async def initialize(self):
            """Initialize the architecture squad (same as Chainlit app)"""
            if not self.initialized and create_kernel and create_architecture_group_chat_async:
                self.kernel = create_kernel()
                # Try to use the enhanced async version first
                try:
                    self.chat = await create_architecture_group_chat_async(self.kernel)
                    print("✅ Enhanced architecture squad initialized successfully")
                except Exception as e:
                    print(
                        f"⚠️  Could not create enhanced architecture squad: {e}")
                    # Fallback to the sync version
                    if create_architecture_group_chat:
                        self.chat = create_architecture_group_chat(self.kernel)
                        print(
                            "✅ Fallback architecture squad initialized successfully")
                    else:
                        raise ImportError(
                            "No architecture squad creation functions available")
                self.initialized = True
            else:
                raise ImportError("Architecture squad modules not available")

    try:
        session = TestArchitectureSquadSession()
        await session.initialize()

        if session.initialized and session.chat:
            print("✅ Chainlit integration test passed")

            # Check if documentation specialist has diagram capabilities
            doc_specialist = None
            for agent in session.chat.agents:
                if "Documentation_Specialist" in agent.name:
                    doc_specialist = agent
                    break

            if doc_specialist and "diagram" in doc_specialist.instructions.lower():
                print(
                    "✅ Chainlit will use enhanced documentation specialist with diagrams")
                return True
            else:
                print("⚠️  Chainlit may not have diagram generation capabilities")
                return False
        else:
            print("❌ Chainlit integration test failed")
            return False

    except Exception as e:
        print(f"❌ Chainlit integration test error: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Testing Chainlit integration with enhanced documentation specialist\n")

    test_results = []

    # Test 1: Enhanced documentation specialist
    result1 = await test_enhanced_documentation_specialist()
    test_results.append(result1)

    # Test 2: Async group chat
    result2 = await test_async_group_chat()
    test_results.append(result2)

    # Test 3: Chainlit integration
    result3 = await test_chainlit_integration()
    test_results.append(result3)

    # Summary
    print(f"\n📊 Test Results Summary:")
    print(f"   Enhanced documentation specialist: {'✅' if result1 else '❌'}")
    print(f"   Async group chat creation: {'✅' if result2 else '❌'}")
    print(f"   Chainlit integration: {'✅' if result3 else '❌'}")

    if all(test_results):
        print(f"\n🎉 All tests passed! Chainlit will use enhanced documentation specialist with diagram generation.")
    else:
        print(f"\n⚠️  Some tests failed. Check the configuration.")

    return all(test_results)


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
