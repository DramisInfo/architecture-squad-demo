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
import shutil
import re
from pathlib import Path

# Add the architecture-squad directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "architecture-squad"))

# Import architecture squad modules with error handling
try:
    from utils import create_kernel, create_architecture_group_chat, create_architecture_group_chat_async
except ImportError as e:
    print(f"Warning: Could not import architecture squad modules: {e}")
    create_kernel = None
    create_architecture_group_chat = None
    create_architecture_group_chat_async = None


class ArchitectureSquadSession:
    """Manages the architecture squad session for a user"""

    def __init__(self):
        self.kernel = None
        self.chat = None
        self.initialized = False
        self.public_dir = Path(__file__).parent / "public" / "diagrams"
        self.public_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize the architecture squad"""
        if not self.initialized and create_kernel and create_architecture_group_chat_async:
            self.kernel = create_kernel()
            # Use the enhanced async version with MCP diagram generation
            try:
                self.chat = await create_architecture_group_chat_async(self.kernel)
                print("✅ Architecture Squad initialized with MCP diagram generation")
            except Exception as e:
                print(
                    f"Warning: Could not create enhanced architecture squad: {e}")
                # Fallback to the sync version
                if create_architecture_group_chat:
                    self.chat = create_architecture_group_chat(self.kernel)
                    print(
                        "⚠️ Fallback to basic architecture squad (no diagram generation)")
                else:
                    raise ImportError(
                        "No architecture squad creation functions available")
            self.initialized = True
        elif not create_kernel or (not create_architecture_group_chat_async and not create_architecture_group_chat):
            raise ImportError(
                "Architecture squad modules not available. Please check your setup.")

    def copy_diagram_to_public(self, original_path: str) -> str:
        """Copy generated diagram to public directory and return the local file path for Chainlit"""
        if not original_path or not os.path.exists(original_path):
            return None

        try:
            # Extract filename from path
            filename = os.path.basename(original_path)

            # Check if file is already in the public directory
            if original_path.startswith(str(self.public_dir)):
                # File is already in public directory, return the path
                return str(self.public_dir / filename)

            # Copy to public directory if not already there
            public_path = self.public_dir / filename
            if not public_path.exists():
                shutil.copy2(original_path, public_path)

            # Return the local file path for Chainlit Image element
            return str(public_path)
        except Exception as e:
            print(f"Error processing diagram file: {e}")
            return None

    def process_diagram_references_in_content(self, content: str) -> tuple:
        """Process content to find diagram file paths and return content with references removed and image elements"""
        diagram_file_paths = []

        # First, check the public diagrams directory to find all available diagrams
        if os.path.exists(self.public_dir):
            for filename in os.listdir(self.public_dir):
                if filename.endswith('.png'):
                    diagram_file_paths.append(str(self.public_dir / filename))

        # If no diagrams were found or public directory doesn't exist, skip further processing
        if not diagram_file_paths:
            return content, []

        # Clean up any diagram references in the content - focus only on paths and .png extension, not specific filenames
        processed_content = re.sub(
            r'\/home\/[^\s]*\/public\/diagrams\/[^\s]*\.png', '', content)
        processed_content = re.sub(r'diagrams\/[^\s]*\.png', '', content)
        processed_content = re.sub(
            r'public\/diagrams\/[^\s]*\.png', '', content)
        # Generic .png file reference
        processed_content = re.sub(r'[^\s]*\.png', '', content)
        processed_content = re.sub(r'\n\s*\n\s*\n', '\n\n', processed_content)

        # Pattern to match file paths in the content (both /tmp and chainlit public directory)
        file_path_patterns = [
            r'/tmp/[^\s]+\.png',
            r'/home/[^\s]*/repos/architecture-squad-demo/chainlit-ui/public/diagrams/[^\s]+\.png',
            r'/home/[^\s]*/public/diagrams/[^\s]+\.png',
            r'public/diagrams/[^\s]+\.png',
            r'diagrams/[^\s]+\.png',
        ]

        diagram_file_paths = []

        # Also look for HTML img tags in the content
        html_img_pattern = r'<img[^>]*src="([^"]*)"[^>]*>'

        # Extract image paths from HTML img tags
        html_img_matches = re.findall(html_img_pattern, content)
        for img_src in html_img_matches:
            if '/public/diagrams/' in img_src:
                # Convert public URL back to local file path
                filename = os.path.basename(img_src)
                local_path = str(self.public_dir / filename)
                if os.path.exists(local_path):
                    diagram_file_paths.append(local_path)

        def replace_file_path(match):
            file_path = match.group(0)

            # Handle case for image paths that don't have the full path
            if file_path.endswith('.png') and not file_path.startswith("/"):
                # Try to find the file in the diagrams directory by filename
                filename = os.path.basename(file_path)
                potential_path = str(self.public_dir / filename)

                # Search the diagrams directory for the file
                if not os.path.exists(potential_path):
                    # If exact filename not found, check if any PNG exists in the diagrams directory
                    if os.path.exists(self.public_dir) and os.listdir(self.public_dir):
                        for existing_file in os.listdir(self.public_dir):
                            if existing_file.endswith('.png'):
                                potential_path = str(
                                    self.public_dir / existing_file)
                                print(
                                    f"Found PNG file in diagrams directory: {potential_path}")
                                break

                if os.path.exists(potential_path):
                    file_path = potential_path

            # Now process the file path as before
            local_path = self.copy_diagram_to_public(file_path)
            if local_path:
                diagram_file_paths.append(local_path)
                # Remove the file path from content - we'll show as image elements instead
                return ""
            return file_path

        # Process each pattern to find raw file paths
        processed_content = content
        for pattern in file_path_patterns:
            processed_content = re.sub(
                pattern, replace_file_path, processed_content)

        # Remove HTML img tags from content since we'll show as image elements
        processed_content = re.sub(html_img_pattern, '', processed_content)

        # Clean up extra whitespace from removed elements
        processed_content = re.sub(r'\n\s*\n\s*\n', '\n\n', processed_content)

        return processed_content, diagram_file_paths

    def is_final_documentation(self, content: str) -> bool:
        """Check if the content appears to be the final comprehensive documentation"""
        # Look for indicators of a comprehensive final document
        final_doc_indicators = [
            "# Executive Summary",
            "## Executive Summary",
            "# System Overview and Objectives",
            "## System Overview and Objectives",
            "# Architecture Overview",
            "## Architecture Overview",
            "# Component Architecture",
            "## Component Architecture",
            "# Security Design",
            "## Security Design",
            "# Data Architecture",
            "## Data Architecture",
            "# Technology Stack",
            "## Technology Stack",
            "# Deployment Guide",
            "## Deployment Guide",
            "# References and Resources",
            "## References and Resources"
        ]

        # Count how many section headers are present
        sections_found = sum(
            1 for indicator in final_doc_indicators if indicator in content)

        # If we find multiple key sections, this is likely the final comprehensive document
        return sections_found >= 4

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

            # Always process diagrams for Documentation Specialist (not just final documents)
            # This ensures diagrams are shown in all Documentation Specialist responses
            if response.name == "Documentation_Specialist":
                processed_content, diagram_file_paths = self.process_diagram_references_in_content(
                    response.content)
                response.content = processed_content
                # Store diagram file paths separately to avoid Pydantic validation issues
                response._diagram_files = diagram_file_paths
                print(
                    f"Found {len(diagram_file_paths)} diagram files: {diagram_file_paths}")

            yield response

        # Reset completion flag for next conversation
        if hasattr(self.chat, 'is_complete'):
            self.chat.is_complete = False


@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    # Create architecture squad session
    squad_session = ArchitectureSquadSession()

    # Store in user session
    cl.user_session.set("squad", squad_session)

    # Welcome message
    welcome_message = """# 🏗️ Welcome to the Architecture Squad!

Our team of **certified solution architects** will collaborate to design your system architecture.

## 👥 Meet Your Architecture Team:

### 🔍 **Platform Specialists**
- **🔍 Platform Selector** - Routes to the right cloud specialist
- **☁️ Azure Solution Architect** - Microsoft Azure certified expert
- **🚀 AWS Solution Architect** - Amazon Web Services certified expert  
- **🐳 Kubernetes Solution Architect** - Container orchestration & OpenShift expert

### 🛠️ **Technical Specialists**
- **🏛️ Solution Architect** - General high-level system design
- **⚙️ Technical Architect** - Detailed technical specifications
- **🔒 Security Architect** - Security design and compliance
- **💾 Data Architect** - Data strategy and storage design
- **📚 Documentation Specialist** - Comprehensive technical documentation **with visual diagram generation** 🎨

## 🚀 How It Works:

1. **Describe your system requirements** (be specific about platform preferences if any)
2. **Platform Selector** analyzes and routes to the appropriate certified specialist
3. **Specialized architects collaborate** to create comprehensive architecture
4. **Documentation Specialist generates visual diagrams** using advanced MCP diagram generation 🎨
5. **Receive detailed documentation** with embedded architecture diagrams tailored to your platform

## 💡 Example Requests:

- *"Design a microservices e-commerce platform using Azure services"*
- *"Create a serverless data processing pipeline on AWS"* 
- *"Design a cloud-native application using Kubernetes and OpenShift"*
- *"I need a scalable web application but not sure which cloud platform to use"*

---

**Ready to start?** Share your project requirements and let our certified architects collaborate on your solution! 🎯
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

            # Special handling for Documentation Specialist with diagrams
            if response.name == "Documentation_Specialist":
                # Check if diagrams were generated
                diagram_file_paths = getattr(response, '_diagram_files', [])

                # Create image elements for all found diagrams
                image_elements = []
                if diagram_file_paths:
                    for file_path in diagram_file_paths:
                        if os.path.exists(file_path):
                            filename = os.path.basename(file_path)
                            print(f"Adding image element: {file_path}")
                            image_element = cl.Image(
                                path=file_path,
                                name=filename,
                                display="inline",
                                size="large"
                            )
                            image_elements.append(image_element)
                        else:
                            print(
                                f"Warning: Image file does not exist: {file_path}")

                # Create message with content and embedded images
                agent_msg = cl.Message(
                    content=f"## {agent_name}\n\n{response.content}",
                    elements=image_elements,
                    author=agent_name
                )
                await agent_msg.send()

                if diagram_file_paths:
                    await cl.Message(
                        content=f"🎨 **{len(diagram_file_paths)} architecture diagram(s) generated and embedded above!**",
                        author="System"
                    ).send()
            else:
                # Create message for other agent responses
                agent_msg = cl.Message(
                    content=f"## {agent_name}\n\n{response.content}",
                    author=agent_name
                )
                await agent_msg.send()

            agent_responses.append(f"✅ {agent_name}")

        # Update thinking message to show completion
        if agent_responses:
            completion_message = f"✅ Architecture Squad collaboration complete!\n\n**Agents that participated:**\n" + \
                "\n".join(agent_responses)

            # Check if diagrams were generated
            if any("Documentation Specialist" in resp for resp in agent_responses):
                completion_message += "\n\n🎨 **Visual architecture diagrams have been generated and displayed above!**"

            # Use a new message instead of updating (which doesn't support content parameter)
            await cl.Message(
                content=completion_message,
                author="System"
            ).send()
        else:
            await cl.Message(
                content="⚠️ No agent responses received. Please try rephrasing your request.",
                author="System"
            ).send()

        # Remove the thinking message
        await thinking_msg.remove()

    except Exception as e:
        await cl.Message(
            content=f"❌ Error during architecture collaboration: {str(e)}",
            author="System"
        ).send()

        # Also send a helpful message
        await cl.Message(
            content="Please check your environment configuration and try again. Make sure all required environment variables are set.",
            author="System"
        ).send()

        # Remove the thinking message
        await thinking_msg.remove()


if __name__ == "__main__":
    # This allows running the app directly with: python app.py
    import chainlit.cli
    chainlit.cli.run_chainlit(__file__)
