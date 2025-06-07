#!/usr/bin/env python3
"""
Comprehensive demo script showcasing the certified solution architects.
This script runs interactive demonstrations of each specialized architect.
"""

from utils import create_kernel, create_architecture_group_chat
import asyncio
import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def run_demo_scenario(chat, scenario_name, requirements, max_responses=4):
    """Run a single demo scenario"""
    print(f"\n{'='*80}")
    print(f"🎯 SCENARIO: {scenario_name}")
    print(f"{'='*80}")
    print(f"📋 Requirements: {requirements}")
    print(f"\n{'🤝 ARCHITECTURE SQUAD COLLABORATION':^80}")
    print("="*80)

    # Reset chat for new scenario
    chat.is_complete = False

    try:
        await chat.add_chat_message(message=requirements)

        response_count = 0
        async for response in chat.invoke():
            if response is None or not response.name:
                continue

            response_count += 1
            agent_name = response.name.replace("_", " ").title()

            print(f"\n## {response_count}. {agent_name}")
            print("-" * 60)
            print(response.content)
            print("-" * 60)

            # Control demo length
            if response_count >= max_responses:
                print(f"\n📝 [Demo continues with remaining specialists...]")
                break

    except Exception as e:
        print(f"❌ Error in scenario: {e}")


async def main():
    """Main demo function"""
    print("🏗️  ARCHITECTURE SQUAD - CERTIFIED SOLUTION ARCHITECTS DEMO")
    print("=" * 80)
    print("Demonstrating platform-specific routing and specialized expertise")
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Initialize architecture squad
    try:
        kernel = create_kernel()
        chat = create_architecture_group_chat(kernel)
        print("✅ Architecture Squad initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize Architecture Squad: {e}")
        return

    # Define comprehensive demo scenarios
    scenarios = [
        {
            "name": "Azure Enterprise E-commerce Platform",
            "requirements": """
            Design an enterprise e-commerce platform for a Fortune 500 retail company. 
            Requirements:
            - Must integrate with existing Microsoft ecosystem (Office 365, Active Directory)
            - Handle 50,000+ concurrent users during peak shopping seasons
            - PCI DSS compliance for payment processing
            - Integration with on-premises ERP system (SAP)
            - Multi-region deployment for global customers
            - Strong preference for Microsoft Azure cloud services
            - Budget: $2M annually for cloud infrastructure
            """,
            "max_responses": 3
        },
        {
            "name": "AWS Serverless Data Analytics Pipeline",
            "requirements": """
            Build a real-time data analytics platform for a fintech startup.
            Requirements:
            - Process 1TB+ of transaction data daily
            - Real-time fraud detection and risk scoring
            - Serverless architecture for cost optimization
            - Global deployment across multiple AWS regions
            - Integration with third-party financial data providers
            - SOC 2 Type II compliance required
            - Prefer AWS services for mature ecosystem and cost control
            - Startup budget constraints - need pay-as-you-grow model
            """,
            "max_responses": 3
        },
        {
            "name": "Multi-Cloud Kubernetes Microservices Platform",
            "requirements": """
            Create a cloud-native microservices platform for a technology company.
            Requirements:
            - Must run across AWS, Azure, and on-premises environments
            - 200+ microservices with complex inter-service communication
            - GitOps-based deployment workflows
            - Container orchestration with Kubernetes/OpenShift
            - Zero-downtime deployments and canary releases
            - Service mesh for security and observability
            - Avoid vendor lock-in - need portability
            - DevOps-first culture with automated CI/CD
            """,
            "max_responses": 3
        },
        {
            "name": "Platform-Agnostic IoT Solution",
            "requirements": """
            Design an IoT data collection and analytics platform.
            Requirements:
            - Connect 100,000+ IoT devices globally
            - Real-time data processing and analytics
            - Machine learning for predictive maintenance
            - Scalable and cost-effective solution
            - No specific cloud platform preference - need recommendation
            - Global deployment with edge computing capabilities
            - Integration with existing manufacturing systems
            """,
            "max_responses": 4
        }
    ]

    # Run each scenario
    for i, scenario in enumerate(scenarios, 1):
        await run_demo_scenario(
            chat=chat,
            scenario_name=scenario["name"],
            requirements=scenario["requirements"],
            max_responses=scenario.get("max_responses", 3)
        )

        # Add pause between scenarios for readability
        if i < len(scenarios):
            print(f"\n{'⏳ Preparing next scenario...':^80}")
            await asyncio.sleep(1)

    # Demo summary
    print(f"\n{'='*80}")
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("The Architecture Squad demonstrated:")
    print("✅ Intelligent platform selection based on requirements")
    print("✅ Azure-certified solutions for Microsoft ecosystem integration")
    print("✅ AWS-certified solutions for serverless and cost optimization")
    print("✅ Kubernetes-certified solutions for cloud-native portability")
    print("✅ Platform-agnostic recommendations when no preference specified")
    print("✅ Collaborative multi-agent architecture design process")
    print("✅ Comprehensive documentation covering all architecture aspects")

    print(f"\n🏗️ Architecture Squad - Certified Solution Architects Ready for Production!")
    print(f"Demo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    # Environment check
    if not os.getenv("GITHUB_TOKEN") and not os.getenv("AZURE_OPENAI_API_KEY"):
        print("⚠️  Environment Configuration Required")
        print("-" * 40)
        print("Please set one of the following environment variables:")
        print("• GITHUB_TOKEN - for GitHub Models API")
        print("• AZURE_OPENAI_API_KEY - for Azure OpenAI API")
        print("\nExample:")
        print("export GITHUB_TOKEN=your_github_token")
        print("export API_HOST=github")
        sys.exit(1)

    # Run the demo
    print("🚀 Starting Architecture Squad Demo...")
    asyncio.run(main())
