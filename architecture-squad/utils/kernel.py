"""
Kernel utilities for creating and configuring Semantic Kernel instances
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
        chat_client = AsyncOpenAI(
            api_key=os.environ["GITHUB_TOKEN"],
            base_url="https://models.inference.ai.azure.com"
        )
        chat_completion_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("GITHUB_MODEL", "gpt-4o"),
            async_client=chat_client
        )

    kernel.add_service(chat_completion_service)
    return kernel
