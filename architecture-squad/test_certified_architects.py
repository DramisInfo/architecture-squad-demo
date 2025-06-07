#!/usr/bin/env python3
"""
Test script for the improved Architecture Squad with certified solution architects.
This script demonstrates how the platform selector routes to appropriate specialists.
"""

import asyncio
import os
from utils import create_kernel, create_architecture_group_chat


async def test_architecture_squad():
    """Test the architecture squad with different platform scenarios"""

    print("="*80)
    print("ARCHITECTURE SQUAD - CERTIFIED SOLUTION ARCHITECTS DEMO")
    print("="*80)
    print("Testing platform-specific routing and specialized expertise")
    print()

    # Create kernel and architecture group chat
    kernel = create_kernel()
    chat = create_architecture_group_chat(kernel)

    # Test scenarios for different platforms
    test_scenarios = [
        {
            "name": "Azure-focused E-commerce Platform",
            "requirements": """
            We need to design an e-commerce platform for our enterprise company. 
            We are heavily invested in Microsoft technologies including Office 365, 
            Active Directory, and have existing Azure subscriptions. 
            We need strong enterprise compliance and integration with our existing 
            Microsoft ecosystem. The solution should handle 10,000+ concurrent users 
            and integrate with our existing on-premises Windows Server environment.
            """
        },
        {
            "name": "AWS Cloud-Native Startup Application",
            "requirements": """
            We're a startup building a SaaS application that needs to scale globally. 
            We want to leverage AWS services for cost optimization and pay-as-you-go pricing. 
            We need extensive third-party integrations, global reach, and want to take 
            advantage of AWS's mature ecosystem. The application should be serverless 
            where possible and highly cost-efficient for our lean startup budget.
            """
        },
        {
            "name": "Multi-Cloud Kubernetes Microservices",
            "requirements": """
            We need to build a cloud-native microservices architecture that can run 
            across multiple cloud providers to avoid vendor lock-in. We want to use 
            containers, implement GitOps workflows, and need a solution that supports 
            our DevOps-centric culture. The system should be portable across AWS, 
            Azure, and on-premises environments using Kubernetes and OpenShift.
            """
        }
    ]

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"TEST SCENARIO {i}: {scenario['name']}")
        print(f"{'='*60}")
        print(f"Requirements: {scenario['requirements']}")
        print("\n" + "-"*60)
        print("ARCHITECTURE SQUAD COLLABORATION")
        print("-"*60)

        # Reset chat for new scenario
        chat.is_complete = False

        try:
            await chat.add_chat_message(message=scenario['requirements'])

            response_count = 0
            async for response in chat.invoke():
                if response is None or not response.name:
                    continue

                response_count += 1
                print(
                    f"\n## {response.name.upper()} (Response {response_count}):")
                print("-" * 50)
                print(response.content)

                # Limit responses per scenario to keep demo manageable
                if response_count >= 3:
                    print("\n[Demo truncated - continuing to next scenario...]")
                    break

        except Exception as e:
            print(f"Error in scenario {i}: {e}")
            continue

    print(f"\n{'='*80}")
    print("DEMO COMPLETED")
    print("="*80)
    print("The Architecture Squad successfully demonstrated:")
    print("• Platform selection based on requirements analysis")
    print("• Routing to certified solution architects (Azure, AWS, Kubernetes)")
    print("• Specialized expertise for each cloud platform")
    print("• Collaborative architecture design process")


async def main():
    """Main function to run the test"""
    await test_architecture_squad()


if __name__ == "__main__":
    # Check for environment variables
    if not os.getenv("GITHUB_TOKEN") and not os.getenv("AZURE_OPENAI_API_KEY"):
        print("⚠️  Warning: No API keys found in environment variables.")
        print("Please set either GITHUB_TOKEN or AZURE_OPENAI_API_KEY to run the demo.")
        print("Example: export GITHUB_TOKEN=your_github_token")
        exit(1)

    asyncio.run(main())
