"""
Architecture Squad Agents

This module contains specialized architecture agents that collaborate
to produce comprehensive architecture documents.
"""

from .platform_selector import create_platform_selector
from .solution_architect import create_solution_architect
from .azure_solution_architect import create_azure_solution_architect
from .aws_solution_architect import create_aws_solution_architect
from .kubernetes_solution_architect import create_kubernetes_solution_architect
from .technical_architect import create_technical_architect
from .security_architect import create_security_architect
from .data_architect import create_data_architect
from .documentation_specialist import create_enhanced_documentation_specialist

__all__ = [
    "create_platform_selector",
    "create_solution_architect",
    "create_azure_solution_architect",
    "create_aws_solution_architect",
    "create_kubernetes_solution_architect",
    "create_technical_architect",
    "create_security_architect",
    "create_data_architect",
    "create_enhanced_documentation_specialist",
]
