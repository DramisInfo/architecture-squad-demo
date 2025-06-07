"""
Simple MCP Server for Azure Documentation Research
Provides web search functionality specifically for Azure documentation
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import re


class AzureResearchMCP:
    """Simple MCP server for Azure documentation research"""

    def __init__(self):
        self.base_url = "https://learn.microsoft.com/en-us/azure"
        self.session = None

        # Azure service catalog for fallback information
        self.azure_services = {
            'app service': {
                'title': 'Azure App Service',
                'url': 'https://learn.microsoft.com/en-us/azure/app-service/',
                'summary': 'Fully managed platform for building, deploying, and scaling web apps and APIs'
            },
            'functions': {
                'title': 'Azure Functions',
                'url': 'https://learn.microsoft.com/en-us/azure/azure-functions/',
                'summary': 'Serverless compute service that runs event-triggered code without managing servers'
            },
            'storage': {
                'title': 'Azure Storage',
                'url': 'https://learn.microsoft.com/en-us/azure/storage/',
                'summary': 'Scalable, secure cloud storage for data, apps, and workloads'
            },
            'sql database': {
                'title': 'Azure SQL Database',
                'url': 'https://learn.microsoft.com/en-us/azure/azure-sql/',
                'summary': 'Fully managed SQL database service with AI-powered features'
            },
            'cosmos db': {
                'title': 'Azure Cosmos DB',
                'url': 'https://learn.microsoft.com/en-us/azure/cosmos-db/',
                'summary': 'Globally distributed, multi-model database service'
            },
            'kubernetes service': {
                'title': 'Azure Kubernetes Service (AKS)',
                'url': 'https://learn.microsoft.com/en-us/azure/aks/',
                'summary': 'Managed Kubernetes service for deploying and managing containerized applications'
            },
            'application gateway': {
                'title': 'Azure Application Gateway',
                'url': 'https://learn.microsoft.com/en-us/azure/application-gateway/',
                'summary': 'Web traffic load balancer with application-level routing and SSL termination'
            },
            'key vault': {
                'title': 'Azure Key Vault',
                'url': 'https://learn.microsoft.com/en-us/azure/key-vault/',
                'summary': 'Secure storage and management of secrets, keys, and certificates'
            }
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def search_azure_docs(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search Azure documentation for relevant information

        Args:
            query: Search query for Azure topics
            max_results: Maximum number of results to return

        Returns:
            Dictionary with search results and summaries
        """
        try:
            # Enhanced Azure-specific search patterns
            azure_patterns = [
                f"Azure {query}",
                f"{query} Azure",
                f"Microsoft Azure {query}",
                f"{query} best practices Azure",
                f"Azure {query} architecture"
            ]

            # Try the most specific pattern first
            best_pattern = azure_patterns[0] if not query.lower(
            ).startswith('azure') else query

            # Use Microsoft Learn search with improved URL
            search_url = f"https://learn.microsoft.com/api/search?search={quote_plus(best_pattern)}&locale=en-us&$top={max_results}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9'
            }

            async with self.session.get(search_url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []

                    for item in data.get('results', [])[:max_results]:
                        # Filter for Azure-specific content
                        url = item.get('url', '')
                        title = item.get('title', '')

                        if any(azure_term in url.lower() or azure_term in title.lower()
                               for azure_term in ['azure', 'microsoft']):
                            result = {
                                'title': title,
                                'url': f"https://learn.microsoft.com{url}" if url.startswith('/') else url,
                                'summary': item.get('summary', ''),
                                'last_modified': item.get('last_modified', ''),
                                'products': item.get('products', ['Azure'])
                            }
                            results.append(result)

                    if results:
                        return {
                            'success': True,
                            'query': query,
                            'results_count': len(results),
                            'results': results
                        }
                    else:
                        # Try fallback with different pattern
                        return await self._fallback_search(query, max_results)
                else:
                    return await self._fallback_search(query, max_results)

        except Exception as e:
            print(f"Search error: {e}")
            return await self._fallback_search(query, max_results)

    async def _fallback_search(self, query: str, max_results: int) -> Dict[str, Any]:
        """Fallback search method using direct web scraping"""
        try:
            # Simple search using site:learn.microsoft.com
            search_query = f"site:learn.microsoft.com/en-us/azure {query}"
            google_url = f"https://www.google.com/search?q={quote_plus(search_query)}&num={max_results}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            async with self.session.get(google_url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    results = []
                    search_results = soup.find_all(
                        'div', class_='g')[:max_results]

                    for result in search_results:
                        title_elem = result.find('h3')
                        link_elem = result.find('a')
                        snippet_elem = result.find(
                            'span', class_=['st', 'aCOpRe'])

                        if title_elem and link_elem:
                            url = link_elem.get('href', '')
                            if 'learn.microsoft.com' in url:
                                results.append({
                                    'title': title_elem.get_text(strip=True),
                                    'url': url,
                                    'summary': snippet_elem.get_text(strip=True) if snippet_elem else '',
                                    'last_modified': '',
                                    'products': ['Azure']
                                })

                    return {
                        'success': True,
                        'query': query,
                        'results_count': len(results),
                        'results': results
                    }

            return {
                'success': False,
                'error': 'No search results found',
                'query': query,
                'results': []
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'results': []
            }

    async def get_azure_service_info(self, service_name: str) -> Dict[str, Any]:
        """
        Get specific information about an Azure service

        Args:
            service_name: Name of the Azure service

        Returns:
            Dictionary with service information
        """
        # First try the catalog for quick lookup
        service_key = service_name.lower().strip()
        if service_key in self.azure_services:
            service_info = self.azure_services[service_key]
            return {
                'success': True,
                'query': f"Azure {service_name}",
                'results_count': 1,
                'results': [service_info]
            }

        # Fall back to search
        query = f"Azure {service_name} overview documentation"
        return await self.search_azure_docs(query, max_results=3)

    def get_service_suggestions(self, partial_name: str) -> List[str]:
        """Get suggestions for Azure services based on partial name"""
        partial_lower = partial_name.lower()
        suggestions = []

        for service_key, service_info in self.azure_services.items():
            if partial_lower in service_key or partial_lower in service_info['title'].lower():
                suggestions.append(service_info['title'])

        return suggestions[:5]  # Return top 5 suggestions


# Simple usage example and test function
async def test_mcp_server():
    """Test the MCP server functionality"""
    async with AzureResearchMCP() as mcp:
        # Test search
        results = await mcp.search_azure_docs("Azure App Service deployment")
        print("Search Results:")
        print(json.dumps(results, indent=2))

        # Test service info
        service_info = await mcp.get_azure_service_info("Functions")
        print("\nService Info:")
        print(json.dumps(service_info, indent=2))


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
