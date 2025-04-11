"""
filepath: backend/main.py
Main FastAPI application entry point for the Modular AI Agent System.
Provides API endpoints and initializes core modules.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import core modules
from .agents import ResearchAgent, registry

# Import API router
from .api import api_router
from .api.agents import router as agents_router
from .llm import LlamaCPPLLM
from .memory import ChromaDBMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize LLM, Memory, and register Agents
    logger.info("Starting up application...")

    # ### TEMPORARILY COMMENTED OUT FOR DEBUGGING ###
    # # Initialize LLM
    # llm_instance = None
    # model_path = os.environ.get("MODEL_PATH")
    # if model_path and os.path.isfile(model_path):
    #     llm_config = {
    #         "model_path": model_path,
    #         "model_params": {"n_ctx": 4096, "n_gpu_layers": -1}, # Use GPU if available
    #         "generate_params": {"temperature": 0.7, "top_p": 0.9},
    #     }
    #     try:
    #         llm_instance = LlamaCPPLLM(config=llm_config)
    #         logger.info(f"LLM initialized using model: {model_path}")
    #     except Exception as e:
    #         logger.error(
    #             f"LLM initialization failed with model {model_path}: {e}. Agent functionality will be limited."
    #         )
    # elif model_path: # Path provided but not found
    #     logger.warning(
    #         f"MODEL_PATH environment variable set to '{model_path}', but file not found. LLM not initialized."
    #     )
    # else: # No path provided
    #     logger.warning(
    #         "MODEL_PATH environment variable not set. LLM not initialized."
    #     )
    #
    # # Initialize Memory
    # memory_instance = None
    # memory_config = {
    #     "persist_directory": ".chroma_db",
    #     "collection_name": "research_agent_memory",
    #     "embedding_model_name": "all-MiniLM-L6-v2", # Example embedding
    # }
    # try:
    #     memory_instance = ChromaDBMemory(config=memory_config)
    #     logger.info("Memory initialized.")
    # except Exception as e:
    #     logger.error(
    #         f"Memory initialization failed: {e}. Agent functionality will be limited."
    #     )
    #     # memory_instance = None # Already None
    #
    # # Register ResearchAgent with LLM and Memory
    # if llm_instance and memory_instance:
    #     try:
    #         research_agent = ResearchAgent(llm=llm_instance, memory=memory_instance)
    #         # Note: We are not using the registry.create_agent method here directly,
    #         # as we are manually instantiating with LLM/Memory.
    #         # If using the registry's create_agent, it would need modification
    #         # to handle dependency injection of LLM/Memory.
    #         registry._agent_instances[research_agent.id] = (
    #             research_agent  # Manual registration
    #         )
    #         logger.info(
    #             f"Registered agent: {research_agent.name} with ID {research_agent.id}"
    #         )
    #     except Exception as e:
    #         logger.error(f"Failed to register ResearchAgent: {e}")
    # else:
    #     logger.warning(
    #         "LLM or Memory not available. Skipping ResearchAgent registration."
    #     )
    ### END TEMPORARY COMMENT ###

    yield
    # Shutdown: Cleanup resources (if needed)
    logger.info("Shutting down application...")
    # Add any cleanup logic here, e.g., closing connections


# Create FastAPI app with lifespan manager
app = FastAPI(
    title="Modular AI Agent System",
    description="A Pythonic, GPU-accelerated, local-first AI research agent framework",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")
app.include_router(agents_router, prefix="/api/v1", tags=["agents"])


# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Modular AI Agent System API is running",
        "version": "0.1.0",
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}


# TODO: Initialize required services on startup
# TODO: Configure shutdown handlers

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
