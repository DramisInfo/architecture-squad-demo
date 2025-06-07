"""
Demo script for the Architecture Squad

This script demonstrates how to use the architecture squad 
for a specific use case - designing an e-commerce platform.
"""

import asyncio
from utils import create_kernel, create_architecture_group_chat


async def demo_ecommerce_architecture():
    """Demo the architecture squad with an e-commerce platform example"""

    # Create kernel and architecture group chat
    kernel = create_kernel()
    chat = create_architecture_group_chat(kernel)

    print("="*80)
    print("ARCHITECTURE SQUAD DEMO: E-COMMERCE PLATFORM")
    print("="*80)
    print()

    # Sample requirement for e-commerce platform
    requirements = """
Design a modern e-commerce platform with the following requirements:

Business Requirements:
- Support 100K daily active users
- Handle 10K concurrent users during peak hours
- Support multiple payment methods (credit cards, PayPal, digital wallets)
- Multi-tenant support for different vendors
- Real-time inventory management
- Order tracking and fulfillment
- Customer reviews and ratings
- Recommendation engine
- Mobile and web interfaces

Technical Requirements:
- High availability (99.9% uptime)
- Fast response times (<200ms for API calls)
- Scalable architecture for future growth
- Secure payment processing
- PCI DSS compliance
- GDPR compliance for European customers
- Analytics and reporting capabilities
- Integration with third-party logistics providers

Business Context:
- Startup company looking to compete with established players
- Limited initial budget but plans for rapid scaling
- Team of 20 developers
- 6-month timeline to MVP
- Plans to expand internationally
"""

    print("Requirements:")
    print("-" * 40)
    print(requirements)
    print("\n" + "="*80)
    print("STARTING ARCHITECTURE COLLABORATION")
    print("="*80)

    # Add the requirements to the chat
    await chat.add_chat_message(message=requirements)

    try:
        async for response in chat.invoke():
            if response is None or not response.name:
                continue
            print()
            print(f"# {response.name.upper()}:")
            print("-" * 40)
            print(response.content)
            print("-" * 80)
    except Exception as e:
        print(f"Error during chat invocation: {e}")

    print("\n" + "="*80)
    print("ARCHITECTURE COLLABORATION COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_ecommerce_architecture())
