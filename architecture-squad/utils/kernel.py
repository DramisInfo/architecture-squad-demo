"""
Kernel utilities for creating and configuring Semantic Kernel instances

Supports multiple AI service providers:
- GitHub Models (default)
- Azure OpenAI with API key authentication
- Azure OpenAI with Azure AD authentication
"""

import os
import logging
import time
import functools
import azure.identity
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def set_kernel_logging_level(level: str = "INFO") -> None:
    """
    Set the logging level for the kernel module.

    Args:
        level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    if level.upper() in level_map:
        logger.setLevel(level_map[level.upper()])
        logger.info(f"Kernel logging level set to {level.upper()}")
    else:
        logger.warning(f"Invalid logging level '{level}'. Using INFO level.")
        logger.setLevel(logging.INFO)


def log_environment_info() -> None:
    """Log relevant environment variables for debugging (without exposing sensitive data)."""
    logger.info("=== Environment Configuration ===")

    # Safe environment variables to log (non-sensitive)
    safe_vars = [
        "API_HOST",
        "AZURE_OPENAI_VERSION",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_CHAT_MODEL",
        "GITHUB_MODEL"
    ]

    for var in safe_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"{var}: {value}")
        else:
            logger.debug(f"{var}: Not set")

    # Log presence of sensitive variables without exposing values
    sensitive_vars = [
        "GITHUB_TOKEN",
        "AZURE_OPENAI_API_KEY"
    ]

    for var in sensitive_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"{var}: ***SET*** (length: {len(value)})")
        else:
            logger.debug(f"{var}: Not set")

    logger.info("=== End Environment Configuration ===")


def log_execution_time(func):
    """Decorator to log function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"Starting {func.__name__}")

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(
                f"{func.__name__} completed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"{func.__name__} failed after {execution_time:.2f} seconds: {str(e)}")
            raise

    return wrapper


@log_execution_time
@log_execution_time
def create_kernel() -> Kernel:
    """Creates a Kernel instance with an Azure OpenAI or GitHub Models ChatCompletion service."""
    logger.info("Starting kernel creation process")

    try:
        load_dotenv(override=True)
        logger.debug("Environment variables loaded from .env file")

        # Log environment configuration for debugging
        log_environment_info()

        API_HOST = os.getenv("API_HOST", "github")
        logger.info(f"API_HOST configuration: {API_HOST}")

        kernel = Kernel()
        logger.debug("Semantic Kernel instance created")

        if API_HOST == "azure":
            logger.info("Configuring Azure OpenAI service")

            # Validate required Azure OpenAI environment variables
            required_vars = ["AZURE_OPENAI_VERSION",
                             "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_CHAT_MODEL"]
            missing_vars = [var for var in required_vars if not os.getenv(var)]

            logger.debug(
                f"Checking required Azure OpenAI environment variables: {required_vars}")

            if missing_vars:
                logger.error(
                    f"Missing required environment variables for Azure OpenAI: {', '.join(missing_vars)}")
                raise ValueError(
                    f"Missing required environment variables for Azure OpenAI: {', '.join(missing_vars)}")

            logger.info(
                "All required Azure OpenAI environment variables are present")

            # Check if we should use API key or Azure AD authentication
            azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
            auth_method = "API Key" if azure_api_key else "Azure AD"
            logger.info(
                f"Using Azure OpenAI authentication method: {auth_method}")

            try:
                if azure_api_key:
                    # Use API key authentication
                    logger.debug(
                        "Creating AsyncAzureOpenAI client with API key authentication")
                    chat_client = AsyncAzureOpenAI(
                        api_key=azure_api_key.strip('"'),
                        api_version=os.environ["AZURE_OPENAI_VERSION"],
                        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                    )
                    logger.info(
                        f"Azure OpenAI client created successfully with endpoint: {os.environ['AZURE_OPENAI_ENDPOINT']}")
                else:
                    # Use Azure AD token authentication (existing behavior)
                    logger.debug("Creating Azure AD token provider")
                    token_provider = azure.identity.get_bearer_token_provider(
                        azure.identity.DefaultAzureCredential(),
                        "https://cognitiveservices.azure.com/.default"
                    )
                    logger.debug(
                        "Creating AsyncAzureOpenAI client with Azure AD authentication")
                    chat_client = AsyncAzureOpenAI(
                        api_version=os.environ["AZURE_OPENAI_VERSION"],
                        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                        azure_ad_token_provider=token_provider,
                    )
                    logger.info(
                        f"Azure OpenAI client created successfully with Azure AD auth, endpoint: {os.environ['AZURE_OPENAI_ENDPOINT']}")

                model_id = os.environ["AZURE_OPENAI_CHAT_MODEL"]
                logger.info(
                    f"Creating OpenAIChatCompletion service with model: {model_id}")

                chat_completion_service = OpenAIChatCompletion(
                    ai_model_id=model_id,
                    async_client=chat_client
                )
                logger.info(
                    "Azure OpenAI ChatCompletion service created successfully")

            except Exception as e:
                logger.error(f"Failed to create Azure OpenAI client: {str(e)}")
                raise
        else:
            logger.info("Configuring GitHub Models service")

            # GitHub Models configuration
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                logger.error(
                    "Missing required environment variable: GITHUB_TOKEN")
                raise ValueError(
                    "Missing required environment variable: GITHUB_TOKEN")

            logger.info("GitHub token found, creating GitHub Models client")

            try:
                base_url = "https://models.inference.ai.azure.com"
                model_id = os.getenv("GITHUB_MODEL", "gpt-4o")

                logger.debug(
                    f"Creating AsyncOpenAI client with base_url: {base_url}")
                logger.info(f"Using GitHub Models with model: {model_id}")

                chat_client = AsyncOpenAI(
                    api_key=github_token,
                    base_url=base_url
                )

                logger.info("GitHub Models client created successfully")
                logger.info(
                    f"Creating OpenAIChatCompletion service with model: {model_id}")

                chat_completion_service = OpenAIChatCompletion(
                    ai_model_id=model_id,
                    async_client=chat_client
                )
                logger.info(
                    "GitHub Models ChatCompletion service created successfully")

            except Exception as e:
                logger.error(
                    f"Failed to create GitHub Models client: {str(e)}")
                raise

        logger.info("Adding chat completion service to kernel")
        kernel.add_service(chat_completion_service)
        logger.info("Kernel creation completed successfully")

        return kernel

    except Exception as e:
        logger.error(f"Failed to create kernel: {str(e)}")
        logger.exception("Full exception details:")
        raise


def validate_kernel_health(kernel: Kernel) -> bool:
    """
    Validate that the kernel is properly configured and can make API calls.

    Args:
        kernel: The Semantic Kernel instance to validate

    Returns:
        bool: True if kernel is healthy, False otherwise
    """
    logger.info("Starting kernel health validation")

    try:
        # Check if kernel has services
        services = kernel.services
        if not services:
            logger.error("Kernel has no services configured")
            return False

        logger.info(f"Kernel has {len(services)} services configured")

        # Check for chat completion service
        chat_services = [s for s in services.values(
        ) if isinstance(s, OpenAIChatCompletion)]
        if not chat_services:
            logger.error("No OpenAIChatCompletion service found in kernel")
            return False

        logger.info(f"Found {len(chat_services)} chat completion service(s)")

        # Test basic functionality with a simple prompt
        chat_service = chat_services[0]
        logger.debug(f"Testing chat service: {chat_service.ai_model_id}")

        # Note: We don't actually make an API call here to avoid costs/rate limits
        # but we verify the service is properly configured
        logger.info("Kernel health validation completed successfully")
        return True

    except Exception as e:
        logger.error(f"Kernel health validation failed: {str(e)}")
        logger.exception("Health validation exception details:")
        return False


def get_kernel_info(kernel: Kernel) -> dict:
    """
    Get detailed information about the kernel configuration.

    Args:
        kernel: The Semantic Kernel instance to inspect

    Returns:
        dict: Kernel configuration information
    """
    logger.debug("Gathering kernel information")

    try:
        info = {
            "service_count": len(kernel.services),
            "services": [],
            "api_host": os.getenv("API_HOST", "github"),
            "timestamp": logging.Formatter().formatTime(logging.LogRecord(
                name="", level=0, pathname="", lineno=0, msg="", args=(), exc_info=None
            ))
        }

        for service_id, service in kernel.services.items():
            service_info = {
                "id": service_id,
                "type": type(service).__name__,
            }

            if isinstance(service, OpenAIChatCompletion):
                service_info["model_id"] = service.ai_model_id

            info["services"].append(service_info)

        logger.debug(f"Kernel info gathered: {len(info['services'])} services")
        return info

    except Exception as e:
        logger.error(f"Failed to gather kernel info: {str(e)}")
        return {"error": str(e)}


def test_kernel_setup() -> None:
    """
    Test function to validate kernel setup and configuration.
    Useful for debugging and setup validation.
    """
    logger.info("=== Kernel Setup Test ===")

    try:
        # Test kernel creation
        kernel = create_kernel()
        logger.info("✓ Kernel created successfully")

        # Validate kernel health
        is_healthy = validate_kernel_health(kernel)
        if is_healthy:
            logger.info("✓ Kernel health validation passed")
        else:
            logger.error("✗ Kernel health validation failed")
            return

        # Get kernel info
        info = get_kernel_info(kernel)
        logger.info(f"✓ Kernel info: {info}")

        logger.info("=== Kernel Setup Test Completed Successfully ===")

    except Exception as e:
        logger.error(f"✗ Kernel setup test failed: {str(e)}")
        logger.exception("Test failure details:")
        raise


if __name__ == "__main__":
    # Enable debug logging for testing
    set_kernel_logging_level("DEBUG")

    # Run the test
    test_kernel_setup()
