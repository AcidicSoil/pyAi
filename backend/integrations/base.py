"""
filepath: backend/integrations/base.py
Base classes for external tool integrations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class IntegrationToolInput(BaseModel):
    """Standard input for an integration tool"""

    parameters: Dict[str, Any]


class IntegrationToolOutput(BaseModel):
    """Standard output for an integration tool"""

    result: Any
    success: bool = True
    error_message: Optional[str] = None


class IntegrationTool(BaseModel):
    """Metadata describing an available tool within an integration"""

    name: str
    description: str
    input_schema: Optional[Dict[str, Any]] = None  # JSON Schema for parameters


class BaseIntegration(ABC):
    """Abstract base class for external integrations (e.g., Slack, Notion)"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__.replace("Integration", "").lower()

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the external service"""
        # TODO: Implement connection logic (e.g., API authentication)
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from the external service"""
        # TODO: Implement disconnection logic
        raise NotImplementedError

    @abstractmethod
    async def list_tools(self) -> List[IntegrationTool]:
        """List available tools provided by this integration"""
        # TODO: Implement tool listing
        raise NotImplementedError

    @abstractmethod
    async def run_tool(
        self, tool_name: str, input_data: IntegrationToolInput
    ) -> IntegrationToolOutput:
        """Run a specific tool provided by this integration"""
        # TODO: Implement tool execution logic
        raise NotImplementedError


# TODO: Implement example subclasses like SlackIntegration, NotionIntegration
# class SlackIntegration(BaseIntegration):
#     async def connect(self) -> bool: pass
#     async def disconnect(self) -> bool: pass
#     async def list_tools(self) -> List[IntegrationTool]:
#         return [IntegrationTool(name='send_message', description='Send a message to a Slack channel')]
#     async def run_tool(self, tool_name: str, input_data: IntegrationToolInput) -> IntegrationToolOutput: pass
