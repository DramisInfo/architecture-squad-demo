"""
Architecture Squad Demo - Multi-Agent System for Collaborative Architecture Design

This implementation follows the Semantic Kernel group chat pattern from Azure Samples
to create specialized architecture agents that collaborate to produce comprehensive
architecture documents.

From full tutorial here:
https://learn.microsoft.com/semantic-kernel/frameworks/agent/examples/example-agent-collaboration?pivots=programming-language-python
"""

import asyncio
from utils import create_kernel, create_architecture_group_chat


async def main():
    # Create kernel and architecture group chat
    kernel = create_kernel()
    chat = create_architecture_group_chat(kernel)

    print("Welcome to the Architecture Squad!")
    print("Provide your system requirements and our specialized architects will collaborate")
    print("to create a comprehensive architecture document.")
    print("\nOur team includes:")
    print("• Solution Architect - High-level system design and patterns")
    print("• Technical Architect - Detailed technical specifications")
    print("• Security Architect - Security design and compliance")
    print("• Data Architect - Data strategy and storage design")
    print("• Documentation Specialist - Comprehensive technical documentation")
    print("\nType 'exit' to quit.\n")

    is_complete = False
    while not is_complete:
        print()
        user_input = input("User > ").strip()
        if not user_input:
            continue

        if user_input.lower() == "exit":
            is_complete = True
            break

        print("\n" + "="*80)
        print("ARCHITECTURE SQUAD COLLABORATION")
        print("="*80)

        await chat.add_chat_message(message=user_input)
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

        # Reset the chat's complete flag for the new conversation round
        chat.is_complete = False


if __name__ == "__main__":
    asyncio.run(main())
