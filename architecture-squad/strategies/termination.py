"""
Agent Termination Strategy - Determines when the collaboration is complete
"""

from semantic_kernel.functions import KernelFunctionFromPrompt


def create_termination_function() -> KernelFunctionFromPrompt:
    """Create the agent termination function"""
    return KernelFunctionFromPrompt(
        function_name="termination",
        prompt="""
Examine the RESPONSE and determine if a complete architecture document has been created.
The document must include all required sections: 
- Executive Summary
- System Overview and Objectives
- Architecture Overview  
- Component Architecture
- Security Design
- Data Architecture
- Technology Stack
- Deployment Guide
- Operational Considerations

If the architecture document is complete and comprehensive, respond: COMPLETE
Otherwise respond: CONTINUE

RESPONSE:
{{$lastmessage}}
""",
    )
