"""
Kernel utilities for creating and configuring Semantic Kernel instances

Supports multiple AI service providers:
- GitHub Models (default)
- Azure OpenAI with API key authentication
- Azure OpenAI with Azure AD authentication
"""

import os
import azure.identity
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


def create_kernel() -> Kernel:
    """Creates a Kernel instance with an Azure OpenAI or GitHub Models ChatCompletion service."""
    load_dotenv(override=True)
    API_HOST = os.getenv("API_HOST", "github")

    kernel = Kernel()

    if API_HOST == "azure":
        # Validate required Azure OpenAI environment variables
        required_vars = ["AZURE_OPENAI_VERSION",
                         "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_CHAT_MODEL"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables for Azure OpenAI: {', '.join(missing_vars)}")

        # Check if we should use API key or Azure AD authentication
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")

        if azure_api_key:
            # Use API key authentication
            chat_client = AsyncAzureOpenAI(
                api_key=azure_api_key,
                api_version=os.environ["AZURE_OPENAI_VERSION"],
                azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            )
        else:
            # Use Azure AD token authentication (existing behavior)
            token_provider = azure.identity.get_bearer_token_provider(
                azure.identity.DefaultAzureCredential(),
                "https://cognitiveservices.azure.com/.default"
            )
            chat_client = AsyncAzureOpenAI(
                api_version=os.environ["AZURE_OPENAI_VERSION"],
                azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                azure_ad_token_provider=token_provider,
            )

        chat_completion_service = OpenAIChatCompletion(
            ai_model_id=os.environ["AZURE_OPENAI_CHAT_MODEL"],
            async_client=chat_client
        )
    else:
        # GitHub Models configuration
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError(
                "Missing required environment variable: GITHUB_TOKEN")

        chat_client = AsyncOpenAI(
            api_key=github_token,
            base_url="https://models.inference.ai.azure.com"
        )
        chat_completion_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("GITHUB_MODEL", "gpt-4o"),
            async_client=chat_client
        )

    kernel.add_service(chat_completion_service)
    return kernel
