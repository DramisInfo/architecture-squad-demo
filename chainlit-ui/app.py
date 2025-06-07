"""
Chainlit UI for Architecture Squad Demo

This provides a web interface for interacting with the multi-agent architecture squad.
Users can submit architecture requirements and see real-time collaboration between
specialized architect agents.
"""

import chainlit as cl
import asyncio
import sys
import os
from pathlib import Path

# Add the architecture-squad directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "architecture-squad"))

# Import architecture squad modules with error handling
try:
    from utils import create_kernel, create_architecture_group_chat
except ImportError as e:
    print(f"Warning: Could not import architecture squad modules: {e}")
    create_kernel = None
    create_architecture_group_chat = None


class ArchitectureSquadSession:
    """Manages the architecture squad session for a user"""

    def __init__(self):
        self.kernel = None
        self.chat = None
        self.initialized = False

    async def initialize(self):
        """Initialize the architecture squad"""
        if not self.initialized and create_kernel and create_architecture_group_chat:
            self.kernel = create_kernel()
            self.chat = create_architecture_group_chat(self.kernel)
            self.initialized = True
        elif not create_kernel or not create_architecture_group_chat:
            raise ImportError(
                "Architecture squad modules not available. Please check your setup.")

    async def process_message(self, message: str):
        """Process a user message through the architecture squad"""
        if not self.initialized:
            await self.initialize()

        # Add user message to chat
        await self.chat.add_chat_message(message=message)

        # Process the conversation and yield agent responses
        async for response in self.chat.invoke():
            if response is None or not response.name:
                continue
            yield response

        # Reset completion flag for next conversation
        self.chat.is_complete = False


@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    # Create architecture squad session
    squad_session = ArchitectureSquadSession()

    # Store in user session
    cl.user_session.set("squad", squad_session)

    # Welcome message
    welcome_message = """# Welcome to the Architecture Squad! 🏗️

I'm your AI-powered architecture team, ready to help you design comprehensive system architectures.

## Our Specialized Team:
- **Solution Architect** - High-level system design and patterns
- **Technical Architect** - Detailed technical specifications  
- **Security Architect** - Security design and compliance
- **Data Architect** - Data strategy and storage design
- **Documentation Specialist** - Comprehensive technical documentation

## How it works:
1. Describe your system requirements or architecture challenge
2. Watch our agents collaborate in real-time
3. Receive a comprehensive architecture document

**What would you like to architect today?**
"""

    await cl.Message(
        content=welcome_message,
        author="Architecture Squad"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming user messages"""
    # Get the architecture squad session
    squad_session = cl.user_session.get("squad")

    if not squad_session:
        await cl.Message(
            content="❌ Session error. Please refresh the page.",
            author="System"
        ).send()
        return

    # Show thinking message
    thinking_msg = cl.Message(
        content="🤔 Architecture Squad is analyzing your requirements...",
        author="System"
    )
    await thinking_msg.send()

    try:
        # Process the message through the architecture squad
        agent_responses = []
        async for response in squad_session.process_message(message.content):
            # Format agent name for display
            agent_name = response.name.replace("_", " ").title()

            # Create message for each agent response
            agent_msg = cl.Message(
                content=f"## {agent_name}\n\n{response.content}",
                author=agent_name
            )
            await agent_msg.send()

            agent_responses.append(f"✅ {agent_name}")

        # Update thinking message to show completion
        if agent_responses:
            await thinking_msg.update(
                content=f"✅ Architecture Squad collaboration complete!\n\n**Agents that participated:**\n" +
                "\n".join(agent_responses)
            )
        else:
            await thinking_msg.update(
                content="⚠️ No agent responses received. Please try rephrasing your request."
            )

    except Exception as e:
        await thinking_msg.update(
            content=f"❌ Error during architecture collaboration: {str(e)}"
        )

        # Also send a helpful message
        await cl.Message(
            content="Please check your environment configuration and try again. Make sure all required environment variables are set.",
            author="System"
        ).send()


if __name__ == "__main__":
    # This allows running the app directly with: python app.py
    import chainlit.cli
    chainlit.cli.run_chainlit(__file__)
