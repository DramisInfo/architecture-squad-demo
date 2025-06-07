"""
Architecture Squad Agents

This module contains specialized architecture agents that collaborate
to produce comprehensive architecture documents.
"""

from .solution_architect import create_solution_architect
from .technical_architect import create_technical_architect
from .security_architect import create_security_architect
from .data_architect import create_data_architect
from .documentation_specialist import create_documentation_specialist

__all__ = [
    "create_solution_architect",
    "create_technical_architect",
    "create_security_architect",
    "create_data_architect",
    "create_documentation_specialist",
]
