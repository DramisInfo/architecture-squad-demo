#!/usr/bin/env python3
"""
Modern test using current Semantic Kernel API
"""

import asyncio
import os
from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIPromptExecutionSettings,
)
from dotenv import load_dotenv


async def test_modern_kernel():
    """Test the modern semantic kernel API"""
    print("Starting test...")
    load_dotenv()
    print("Environment loaded")

    # Create kernel
    print("Creating kernel...")
    kernel = Kernel()
    print("Kernel created")

    # Create OpenAI client
    print("Creating OpenAI client...")
    client = AsyncOpenAI(
        api_key=os.getenv("GITHUB_TOKEN"),
        base_url="https://models.inference.ai.azure.com"
    )
    print("OpenAI client created")

    # Add chat completion service
    print("Creating chat completion service...")
    chat_completion = OpenAIChatCompletion(
        ai_model_id=os.getenv("GITHUB_MODEL", "gpt-4o"),
        async_client=client
    )
    print("Chat completion service created")

    print("Adding service to kernel...")
    kernel.add_service(chat_completion)
    print("Service added to kernel")

    print("✓ Kernel and chat completion service created")

    # Test basic chat
    execution_settings = OpenAIPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    history = ChatHistory()
    history.add_user_message(
        "Hello! Can you help me design a simple web application?")

    print("Making API call...")
    result = await chat_completion.get_chat_message_content(
        chat_history=history,
        settings=execution_settings,
        kernel=kernel,
    )

    print(f"✓ Response: {result.content}")

if __name__ == "__main__":
    asyncio.run(test_modern_kernel())
