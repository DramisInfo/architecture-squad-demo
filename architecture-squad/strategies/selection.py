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
- Solution_Architect
- Technical_Architect
- Security_Architect
- Data_Architect
- Documentation_Specialist

Rules:
- If RESPONSE is user requirements, start with Solution_Architect
- If RESPONSE is from Solution_Architect, move to Technical_Architect
- If RESPONSE is from Technical_Architect, move to Security_Architect
- If RESPONSE is from Security_Architect, move to Data_Architect
- If RESPONSE is from Data_Architect, move to Documentation_Specialist
- If more clarification needed, return to appropriate specialist

RESPONSE:
{{$lastmessage}}
""",
    )
