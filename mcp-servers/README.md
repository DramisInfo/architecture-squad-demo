# Azure Research MCP Server

This is a simple Model Context Protocol (MCP) server that provides Azure documentation research capabilities for the Architecture Squad.

## Features

- **Azure Documentation Search**: Search official Azure documentation at https://learn.microsoft.com/en-us/azure
- **Service Information Lookup**: Get detailed information about specific Azure services
- **Fallback Search**: Uses web search as a fallback when direct API access isn't available

## Usage

### Standalone Usage

```python
import asyncio
from azure_research_mcp import AzureResearchMCP

async def main():
    async with AzureResearchMCP() as mcp:
        # Search for Azure topics
        results = await mcp.search_azure_docs("Azure App Service deployment")
        print(results)
        
        # Get service information
        service_info = await mcp.get_azure_service_info("Functions")
        print(service_info)

asyncio.run(main())
```

### Integration with Azure Architect

The MCP server is automatically integrated with the Azure Solution Architect agent through the `AzureResearchPlugin`. The architect can use these functions:

- `research_azure_topic(topic: str)` - Research Azure topics and best practices
- `get_azure_service_info(service_name: str)` - Get detailed Azure service information

## API Methods

### `search_azure_docs(query: str, max_results: int = 5)`

Searches Azure documentation for the given query.

**Parameters:**
- `query`: Search terms for Azure topics
- `max_results`: Maximum number of results to return (default: 5)

**Returns:**
```python
{
    "success": bool,
    "query": str,
    "results_count": int,
    "results": [
        {
            "title": str,
            "url": str,
            "summary": str,
            "last_modified": str,
            "products": list
        }
    ]
}
```

### `get_azure_service_info(service_name: str)`

Gets specific information about an Azure service.

**Parameters:**
- `service_name`: Name of the Azure service

**Returns:**
Same format as `search_azure_docs`

## Implementation Notes

- The server first tries to use the Microsoft Learn API
- Falls back to web scraping if the API is unavailable
- Handles errors gracefully and returns informative error messages
- Uses async/await pattern for non-blocking operations

## Requirements

```
aiohttp
beautifulsoup4
```

## Testing

Run the server directly to test functionality:

```bash
cd mcp-servers
python azure_research_mcp.py
```

This will run basic tests of the search and service info functions.
