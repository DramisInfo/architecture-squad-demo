"""
Architecture Squad Strategies

This module contains the selection and termination strategies
for coordinating agent collaboration.
"""

from .selection import create_selection_function
from .termination import create_termination_function

__all__ = [
    "create_selection_function",
    "create_termination_function",
]
