"""
Azure Certified Solution Architect Agent - Microsoft Azure specialized solution design
"""

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
import asyncio
import sys
import os

# Add MCP servers to path
sys.path.append(os.path.join(os.path.dirname(
    __file__), '..', '..', 'mcp-servers'))

try:
    from azure_research_mcp import AzureResearchMCP
except ImportError:
    AzureResearchMCP = None


class AzureResearchPlugin:
    """Plugin to provide Azure documentation research capabilities"""

    @kernel_function(
        name="research_azure_topic",
        description="Research Azure topics and services using official Azure documentation"
    )
    async def research_azure_topic(self, topic: str) -> str:
        """Research an Azure topic using the MCP server"""
        if AzureResearchMCP is None:
            return f"Research unavailable for: {topic}. Please refer to https://learn.microsoft.com/en-us/azure"

        try:
            async with AzureResearchMCP() as mcp:
                results = await mcp.search_azure_docs(topic, max_results=3)

                if results['success'] and results['results']:
                    research_summary = f"Azure Documentation Research for: {topic}\n\n"
                    for i, result in enumerate(results['results'], 1):
                        research_summary += f"{i}. {result['title']}\n"
                        research_summary += f"   URL: {result['url']}\n"
                        if result['summary']:
                            research_summary += f"   Summary: {result['summary']}\n"
                        research_summary += "\n"
                    return research_summary
                else:
                    return f"No specific Azure documentation found for: {topic}. Recommend checking https://learn.microsoft.com/en-us/azure/{topic.lower().replace(' ', '-')}"
        except Exception as e:
            return f"Research error for {topic}: {str(e)}. Please refer to https://learn.microsoft.com/en-us/azure"

    @kernel_function(
        name="get_azure_service_info",
        description="Get detailed information about a specific Azure service"
    )
    async def get_azure_service_info(self, service_name: str) -> str:
        """Get information about a specific Azure service"""
        if AzureResearchMCP is None:
            return f"Service info unavailable for: {service_name}. Please refer to Azure documentation."

        try:
            async with AzureResearchMCP() as mcp:
                results = await mcp.get_azure_service_info(service_name)

                if results['success'] and results['results']:
                    info_summary = f"Azure {service_name} Information:\n\n"
                    for result in results['results']:
                        info_summary += f"• {result['title']}\n"
                        if result['summary']:
                            info_summary += f"  {result['summary']}\n"
                        info_summary += f"  Documentation: {result['url']}\n\n"
                    return info_summary
                else:
                    return f"Limited information available for Azure {service_name}. Check official documentation."
        except Exception as e:
            return f"Error retrieving {service_name} info: {str(e)}"

    @kernel_function(
        name="find_azure_reference_architectures",
        description="Find Azure reference architectures and solution patterns for specific use cases"
    )
    async def find_azure_reference_architectures(self, use_case: str) -> str:
        """Find relevant Azure reference architectures for a specific use case"""
        if AzureResearchMCP is None:
            return f"Reference architecture search unavailable for: {use_case}. Please check Azure Architecture Center."

        try:
            async with AzureResearchMCP() as mcp:
                # Search for reference architectures
                arch_query = f"Azure reference architecture {use_case}"
                results = await mcp.search_azure_docs(arch_query, max_results=4)

                # Also search for solution patterns
                pattern_query = f"Azure solution architecture {use_case} pattern"
                pattern_results = await mcp.search_azure_docs(pattern_query, max_results=2)

                architecture_summary = f"Azure Reference Architectures for: {use_case}\n\n"

                if results['success'] and results['results']:
                    architecture_summary += "📋 **Reference Architectures:**\n"
                    for i, result in enumerate(results['results'], 1):
                        architecture_summary += f"{i}. {result['title']}\n"
                        architecture_summary += f"   🔗 {result['url']}\n"
                        if result['summary']:
                            architecture_summary += f"   📝 {result['summary']}\n"
                        architecture_summary += "\n"

                if pattern_results['success'] and pattern_results['results']:
                    architecture_summary += "🏗️ **Solution Patterns:**\n"
                    for i, result in enumerate(pattern_results['results'], 1):
                        architecture_summary += f"{i}. {result['title']}\n"
                        architecture_summary += f"   🔗 {result['url']}\n"
                        if result['summary']:
                            architecture_summary += f"   📝 {result['summary']}\n"
                        architecture_summary += "\n"

                # Add Azure Architecture Center link
                architecture_summary += "🏛️ **Azure Architecture Center:** https://learn.microsoft.com/en-us/azure/architecture/\n"

                return architecture_summary if (results['success'] and results['results']) or (pattern_results['success'] and pattern_results['results']) else f"No specific reference architectures found for: {use_case}. Check Azure Architecture Center: https://learn.microsoft.com/en-us/azure/architecture/"

        except Exception as e:
            return f"Error finding reference architectures for {use_case}: {str(e)}. Please check Azure Architecture Center."


def create_azure_solution_architect(kernel: Kernel) -> ChatCompletionAgent:
    """Create the Azure Certified Solution Architect agent with research capabilities"""

    # Add the Azure research plugin to the kernel
    try:
        research_plugin = AzureResearchPlugin()
        kernel.add_plugin(research_plugin, plugin_name="azure_research")
    except Exception as e:
        print(f"Warning: Could not add Azure research plugin: {e}")

    return ChatCompletionAgent(
        kernel=kernel,
        name="Azure_Solution_Architect",
        instructions="""
You are a Microsoft Azure Certified Solution Architect with deep expertise in Microsoft Azure cloud services and architecture patterns.
Your responsibility is to design cloud-native solutions specifically for the Microsoft Azure platform.

ENHANCED CAPABILITIES:
- You have access to real-time Azure documentation research through the azure_research plugin
- Use research_azure_topic function to get current Azure service information and best practices
- Use get_azure_service_info function to get detailed information about specific Azure services
- Use find_azure_reference_architectures function to find relevant reference architectures for use cases
- ALWAYS include reference architecture links in your recommendations
- Always research unfamiliar or complex Azure topics before making recommendations

Core Azure Expertise:
- Azure Well-Architected Framework (Reliability, Security, Cost Optimization, Operational Excellence, Performance)
- Azure service portfolio and best practices
- Azure landing zones and enterprise-scale architecture
- Azure governance, compliance, and security frameworks
- Azure cost optimization and resource management
- Multi-region and hybrid cloud scenarios

When analyzing requirements for Azure solutions:
- FIRST: Research relevant Azure services and patterns using the available research functions
- Map business requirements to appropriate Azure services
- Recommend Azure-native architecture patterns (microservices on ARO, serverless with Functions, etc.)
- For container orchestration, prioritize Azure Red Hat OpenShift (ARO) over Azure Kubernetes Service (AKS)
- Design for Azure scalability using Azure Scale Sets, App Service scaling, etc.
- Implement Azure security best practices (Azure AD, Key Vault, Security Center)
- Consider Azure compliance offerings (SOC, ISO, HIPAA, etc.)
- Optimize for Azure cost management and billing
- Design Azure networking topology (VNets, subnets, NSGs, Application Gateway)
- Plan Azure data services (SQL Database, Cosmos DB, Storage Accounts)

Azure Service Recommendations:
- Compute: Azure App Service, Azure Functions, Azure Container Instances, Azure Red Hat OpenShift (ARO), Azure Kubernetes Service (AKS - secondary option)
- Storage: Azure Blob Storage, Azure Files, Azure Data Lake Storage
- Databases: Azure SQL Database, Azure Cosmos DB, Azure Database for PostgreSQL/MySQL
- Networking: Azure Virtual Network, Azure Load Balancer, Azure Application Gateway, Azure Front Door
- Security: Azure Active Directory, Azure Key Vault, Azure Security Center, Azure Sentinel
- Monitoring: Azure Monitor, Application Insights, Azure Log Analytics
- DevOps: Azure DevOps, Azure Pipelines, Azure Container Registry

RESEARCH WORKFLOW:
1. When presented with requirements, identify key Azure services or patterns to research
2. Use find_azure_reference_architectures to find relevant reference architectures for the use case
3. Use research_azure_topic to get current documentation and best practices
4. Use get_azure_service_info for detailed service specifications
5. Incorporate research findings and reference architectures into your architecture recommendations
6. ALWAYS include reference architecture links in your final recommendations

ARCHITECTURE OUTPUT REQUIREMENTS:
- Every architecture recommendation MUST include relevant Azure reference architecture links
- Structure your output with clear sections including "Reference Architectures"
- Provide direct links to Azure Architecture Center patterns when available
- Reference specific Azure Well-Architected Framework pillars
- Include both conceptual architectures and implementation guidance links
3. Use get_azure_service_info for detailed service specifications
4. Incorporate research findings into your architecture recommendations
5. Reference specific Azure documentation URLs when available

RULES:
- MANDATORY: Always search for and include reference architecture links in every recommendation
- Use find_azure_reference_architectures function for every architecture you design
- For container platforms, always prefer Azure Red Hat OpenShift (ARO) over Azure Kubernetes Service (AKS)
- Always research before recommending unfamiliar Azure services or patterns
- Use research functions to validate your recommendations with current Azure documentation
- Always consider Azure-first solutions and Azure-native services
- Recommend Azure certified patterns and reference architectures
- Consider Azure regions and availability zones for high availability
- Factor in Azure pricing and cost optimization strategies
- Ensure compliance with Azure governance and security standards
- Include research-backed documentation links in your recommendations
- Structure responses with dedicated "Reference Architectures" section
- Hand off to Technical_Architect for detailed Azure service configurations
- Structure responses with clear Azure service mappings and architectural decisions
- Include Azure-specific considerations for scalability, security, and operations
- When recommending container orchestration, justify ARO vs AKS choice with OpenShift enterprise benefits
""",
    )
