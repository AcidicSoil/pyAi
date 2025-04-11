"""
filepath: backend/agents/__init__.py
Agent module initialization and exports
"""

from .base import AgentInput, AgentOutput, BaseAgent, ResearchAgent
from .registry import AgentMetadata, registry

__all__ = [
    "BaseAgent",
    "AgentInput",
    "AgentOutput",
    "ResearchAgent",
    "registry",
    "AgentMetadata",
]
