"""
Agent Selection Strategy - Determines which agent should take the next turn
"""

from semantic_kernel.functions import KernelFunctionFromPrompt


def create_selection_function() -> KernelFunctionFromPrompt:
    """Create the agent selection function"""
    return KernelFunctionFromPrompt(
        function_name="selection",
        prompt="""
Examine the RESPONSE and choose the next architect agent.
State only the agent name without explanation.

Choose from:
- Platform_Selector
- Solution_Architect
- Azure_Solution_Architect
- AWS_Solution_Architect
- Kubernetes_Solution_Architect
- Technical_Architect
- Security_Architect
- Data_Architect
- Documentation_Specialist

Rules:
- If RESPONSE is user requirements (first message), start with Platform_Selector
- If RESPONSE is from Platform_Selector, route to the recommended specialist architect
- If RESPONSE is from any Solution Architect, move to Technical_Architect
- If RESPONSE is from Technical_Architect, move to Security_Architect
- If RESPONSE is from Security_Architect, move to Data_Architect
- If RESPONSE is from Data_Architect, move to Documentation_Specialist
- If more platform-specific clarification needed, return to appropriate Solution Architect
- If general clarification needed, return to Solution_Architect

Platform Routing (from Platform_Selector responses):
- If recommendation is "Azure_Solution_Architect", choose Azure_Solution_Architect
- If recommendation is "AWS_Solution_Architect", choose AWS_Solution_Architect
- If recommendation is "Kubernetes_Solution_Architect", choose Kubernetes_Solution_Architect
- If recommendation is "Solution_Architect", choose Solution_Architect

RESPONSE:
{{$lastmessage}}
""",
    )
