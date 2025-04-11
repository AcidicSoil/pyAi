"""
filepath: backend/memory/chroma_memory.py
Implementation of the BaseMemory interface using ChromaDB.
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from .base import BaseMemory, MemoryRecord

logger = logging.getLogger(__name__)


class ChromaDBMemory(BaseMemory):
    """Memory provider using ChromaDB for storage and retrieval"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.persist_directory = config.get("persist_directory", ".chroma_db")
        self.collection_name = config.get("collection_name", "agent_memory")
        self.embedding_model_name = config.get(
            "embedding_model_name", "all-MiniLM-L6-v2"
        )

        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False),  # Disable telemetry
            )

            # Use a sentence transformer embedding function
            self.embedding_function = (
                embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name=self.embedding_model_name
                )
            )

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"},  # Use cosine distance
            )
            logger.info(
                f"Initialized ChromaDB client. Collection: {self.collection_name}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB client: {e}")
            raise

    async def add(self, record: MemoryRecord) -> None:
        """Add a record to the ChromaDB collection"""
        try:
            record_id = record.id or str(uuid.uuid4())
            metadata = record.metadata or {}
            metadata["timestamp"] = record.timestamp.isoformat()
            if record.agent_id:
                metadata["agent_id"] = record.agent_id

            self.collection.add(
                ids=[record_id], documents=[record.content], metadatas=[metadata]
            )
            logger.debug(f"Added record {record_id} to ChromaDB")
        except Exception as e:
            logger.error(f"Error adding record to ChromaDB: {e}")
            # Optionally re-raise or handle

    async def get(self, record_id: str) -> Optional[MemoryRecord]:
        """Retrieve a record by ID from ChromaDB"""
        try:
            result = self.collection.get(
                ids=[record_id], include=["metadatas", "documents"]
            )
            if result and result["ids"]:
                retrieved_id = result["ids"][0]
                doc = result["documents"][0]
                meta = result["metadatas"][0]

                # Convert timestamp back
                timestamp = datetime.fromisoformat(
                    meta.pop("timestamp", datetime.utcnow().isoformat())
                )
                agent_id = meta.pop("agent_id", None)

                return MemoryRecord(
                    id=retrieved_id,
                    content=doc,
                    metadata=meta,
                    timestamp=timestamp,
                    agent_id=agent_id,
                )
            return None
        except Exception as e:
            logger.error(f"Error getting record {record_id} from ChromaDB: {e}")
            return None

    async def search(
        self, query: str, top_k: int = 5, filter: Optional[Dict[str, Any]] = None
    ) -> List[MemoryRecord]:
        """Search ChromaDB for relevant records using embeddings"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filter,  # Pass the filter directly to ChromaDB
                include=["metadatas", "documents"],
            )

            records = []
            if results and results["ids"][0]:
                for i in range(len(results["ids"][0])):
                    record_id = results["ids"][0][i]
                    doc = results["documents"][0][i]
                    meta = results["metadatas"][0][i]

                    timestamp = datetime.fromisoformat(
                        meta.pop("timestamp", datetime.utcnow().isoformat())
                    )
                    agent_id = meta.pop("agent_id", None)

                    records.append(
                        MemoryRecord(
                            id=record_id,
                            content=doc,
                            metadata=meta,
                            timestamp=timestamp,
                            agent_id=agent_id,
                        )
                    )
            return records
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            return []

    async def delete(self, record_id: str) -> bool:
        """Delete a record by ID from ChromaDB"""
        try:
            self.collection.delete(ids=[record_id])
            logger.debug(f"Deleted record {record_id} from ChromaDB")
            return True
        except Exception as e:
            logger.error(f"Error deleting record {record_id} from ChromaDB: {e}")
            return False

    async def clear(self, agent_id: Optional[str] = None) -> None:
        """Clear memory in ChromaDB, optionally filtered by agent_id"""
        try:
            if agent_id:
                # Delete records associated with a specific agent
                self.collection.delete(where={"agent_id": agent_id})
                logger.info(f"Cleared memory for agent {agent_id} in ChromaDB")
            else:
                # Clear the entire collection - Use with caution!
                # This might not be what's intended. Consider deleting all items instead.
                logger.warning(
                    "Clearing entire ChromaDB collection. This is potentially destructive."
                )
                # A safer approach might be to query all IDs and delete them:
                # all_ids = self.collection.get()['ids']
                # if all_ids:
                #     self.collection.delete(ids=all_ids)
                # For now, let's just log a warning.
                # If full clear is needed, consider client.delete_collection()
                pass
        except Exception as e:
            logger.error(f"Error clearing ChromaDB memory: {e}")
