"""
filepath: backend/agents/registry.py
Registry system for managing agent instances and types.
"""

from typing import Dict, List, Type

from pydantic import BaseModel

from .base import AgentInput, AgentOutput, BaseAgent


class AgentMetadata(BaseModel):
    """Metadata for registered agents"""

    name: str
    description: str
    capabilities: List[str]
    agent_type: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Research Agent",
                    "description": "Performs web research and summarization",
                    "capabilities": ["web_search", "summarization"],
                    "agent_type": "research",
                }
            ]
        }
    }


class AgentRegistry:
    """Global registry for managing agent types and instances"""

    def __init__(self):
        self._agent_types: Dict[str, Type[BaseAgent]] = {}
        self._agent_instances: Dict[str, BaseAgent] = {}

    def register_agent_type(
        self, agent_type: str, agent_class: Type[BaseAgent]
    ) -> None:
        """Register a new agent type"""
        if agent_type in self._agent_types:
            raise ValueError(f"Agent type {agent_type} already registered")
        self._agent_types[agent_type] = agent_class

    def create_agent(self, agent_type: str, name: str, **kwargs) -> BaseAgent:
        """Create a new agent instance"""
        if agent_type not in self._agent_types:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent_class = self._agent_types[agent_type]
        agent = agent_class(name=name, **kwargs)
        self._agent_instances[agent.id] = agent
        return agent

    def get_agent(self, agent_id: str) -> BaseAgent:
        """Get an agent instance by ID"""
        if agent_id not in self._agent_instances:
            raise ValueError(f"Agent not found: {agent_id}")
        return self._agent_instances[agent_id]

    def list_agents(self) -> List[AgentMetadata]:
        """List all registered agent instances"""
        return [
            AgentMetadata(
                name=agent.name,
                description=agent.description,
                capabilities=agent.capabilities,
                agent_type=agent.__class__.__name__.lower().replace("agent", ""),
            )
            for agent in self._agent_instances.values()
        ]

    def list_agent_types(self) -> List[str]:
        """List available agent types"""
        return list(self._agent_types.keys())


# Global registry instance
registry = AgentRegistry()

# Register built-in agent types
from .base import ResearchAgent

registry.register_agent_type("research", ResearchAgent)
