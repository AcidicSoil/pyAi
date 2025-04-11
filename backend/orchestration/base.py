"""
filepath: backend/orchestration/base.py
Base class for agent orchestration systems.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from ..agents import AgentInput, AgentOutput  # Assuming agents module exists


class Task(BaseModel):
    """Represents a task within an orchestration flow"""

    task_id: str
    agent_id: str
    input_data: AgentInput
    dependencies: List[str] = []  # List of task_ids this task depends on
    status: str = "pending"  # e.g., pending, running, completed, failed


class FlowResult(BaseModel):
    """Represents the final result of an orchestrated flow"""

    flow_id: str
    outputs: Dict[str, AgentOutput]  # Map of task_id to AgentOutput
    status: str = "completed"  # e.g., completed, failed, cancelled
    error_message: Optional[str] = None


class BaseOrchestrator(ABC):
    """Abstract base class for orchestration engines (e.g., Prefect)"""

    @abstractmethod
    async def run_flow(self, tasks: List[Task]) -> FlowResult:
        """Define and run an orchestration flow with the given tasks"""
        # TODO: Implement flow definition and execution (e.g., using Prefect @flow)
        raise NotImplementedError

    @abstractmethod
    async def get_flow_status(self, flow_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a running or completed flow"""
        # TODO: Implement status retrieval (e.g., using Prefect client)
        raise NotImplementedError

    @abstractmethod
    async def cancel_flow(self, flow_id: str) -> bool:
        """Cancel a running flow"""
        # TODO: Implement flow cancellation
        raise NotImplementedError


# TODO: Implement PrefectOrchestrator subclass
# from prefect import flow, task
# from ..agents import registry as agent_registry
#
# class PrefectOrchestrator(BaseOrchestrator):
#     @task
#     async def run_agent_task(self, agent_id: str, input_data: AgentInput):
#         agent = agent_registry.get_agent(agent_id)
#         return await agent.run(input_data)
#
#     @flow
#     async def dynamic_flow(self, tasks_data: List[Dict]):
#         results = {}
#         task_futures = {}
#
#         # TODO: Build Prefect task graph based on dependencies
#         for task_info in tasks_data:
#             # task_futures[task_info['task_id']] = self.run_agent_task.submit(...)
#             pass
#
#         # TODO: Collect results
#         return results
#
#     async def run_flow(self, tasks: List[Task]) -> FlowResult:
#         # Convert Task models to dicts for Prefect flow
#         tasks_data = [t.dict() for t in tasks]
#         # Run the dynamic flow
#         # flow_run = await self.dynamic_flow(tasks_data)
#         pass
#
#     async def get_flow_status(self, flow_id: str) -> Optional[Dict[str, Any]]:
#         pass
#
#     async def cancel_flow(self, flow_id: str) -> bool:
#         pass
