"""
Group chat utilities for creating and configuring the agent group chat
"""

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.agents.strategies import (
    KernelFunctionSelectionStrategy,
    KernelFunctionTerminationStrategy,
)
# Note: ChatHistoryTruncationReducer may not be available in all versions
# We'll implement chat without it for now

from agents import (
    create_platform_selector,
    create_solution_architect,
    create_azure_solution_architect,
    create_aws_solution_architect,
    create_kubernetes_solution_architect,
    create_technical_architect,
    create_security_architect,
    create_data_architect,
    create_documentation_specialist,
)
from strategies import create_selection_function, create_termination_function


def create_architecture_group_chat(kernel: Kernel) -> AgentGroupChat:
    """Create the architecture squad group chat with all agents and strategies"""

    # Create all architecture agents
    platform_selector = create_platform_selector(kernel)
    solution_architect = create_solution_architect(kernel)
    azure_solution_architect = create_azure_solution_architect(kernel)
    aws_solution_architect = create_aws_solution_architect(kernel)
    kubernetes_solution_architect = create_kubernetes_solution_architect(
        kernel)
    technical_architect = create_technical_architect(kernel)
    security_architect = create_security_architect(kernel)
    data_architect = create_data_architect(kernel)
    documentation_specialist = create_documentation_specialist(kernel)

    # Create selection and termination functions
    selection_function = create_selection_function()
    termination_function = create_termination_function()

    # Create the AgentGroupChat with selection and termination strategies
    chat = AgentGroupChat(
        agents=[
            platform_selector,
            solution_architect,
            azure_solution_architect,
            aws_solution_architect,
            kubernetes_solution_architect,
            technical_architect,
            security_architect,
            data_architect,
            documentation_specialist
        ],
        selection_strategy=KernelFunctionSelectionStrategy(
            initial_agent=platform_selector,
            function=selection_function,
            kernel=kernel,
            result_parser=lambda result: str(result.value[0]).strip(
            ) if result.value[0] is not None else "Solution_Architect",
            history_variable_name="lastmessage",
        ),
        termination_strategy=KernelFunctionTerminationStrategy(
            agents=[documentation_specialist],
            function=termination_function,
            kernel=kernel,
            result_parser=lambda result: "COMPLETE" in str(
                result.value[0]).upper(),
            history_variable_name="lastmessage",
            maximum_iterations=20,
        ),
    )

    return chat
