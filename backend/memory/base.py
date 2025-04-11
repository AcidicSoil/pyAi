"""
filepath: backend/memory/base.py
Base class for agent memory systems.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    """Represents a single record in the memory"""

    id: str
    content: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_id: Optional[str] = None


class BaseMemory(ABC):
    """Abstract base class for different memory implementations"""

    @abstractmethod
    async def add(self, record: MemoryRecord) -> None:
        """Add a record to memory"""
        # TODO: Implement add logic
        raise NotImplementedError

    @abstractmethod
    async def get(self, record_id: str) -> Optional[MemoryRecord]:
        """Retrieve a record by ID"""
        # TODO: Implement get logic
        raise NotImplementedError

    @abstractmethod
    async def search(
        self, query: str, top_k: int = 5, filter: Optional[Dict[str, Any]] = None
    ) -> List[MemoryRecord]:
        """Search memory for relevant records"""
        # TODO: Implement search logic (e.g., using ChromaDB embeddings)
        raise NotImplementedError

    @abstractmethod
    async def delete(self, record_id: str) -> bool:
        """Delete a record by ID"""
        # TODO: Implement delete logic
        raise NotImplementedError

    @abstractmethod
    async def clear(self, agent_id: Optional[str] = None) -> None:
        """Clear memory, optionally for a specific agent"""
        # TODO: Implement clear logic
        raise NotImplementedError


# TODO: Implement ChromaDBMemory subclass
# class ChromaDBMemory(BaseMemory):
#     def __init__(self, config: Dict[str, Any]):
#         # Initialize ChromaDB client
#         pass
#
#     async def add(self, record: MemoryRecord) -> None:
#         pass
#
#     async def get(self, record_id: str) -> Optional[MemoryRecord]:
#         pass
#
#     async def search(self, query: str, top_k: int = 5, filter: Optional[Dict[str, Any]] = None) -> List[MemoryRecord]:
#         pass
#
#     async def delete(self, record_id: str) -> bool:
#         pass
#
#     async def clear(self, agent_id: Optional[str] = None) -> None:
#         pass
