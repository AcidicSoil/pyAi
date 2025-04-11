# Modular AI Agent System - Backend

This directory contains the FastAPI-based backend for the Modular AI Agent System.

## Structure

- `api/`: API endpoints and routers
- `agents/`: Agent implementations
- `llm/`: Language model interfaces
- `memory/`: Memory and storage interfaces
- `orchestration/`: Agent orchestration with Prefect
- `integrations/`: External service integrations
- `main.py`: FastAPI application entry point

## Setup

### Prerequisites

- Python 3.11+
- Vulkan-compatible GPU for LLM acceleration
- (Optional) CUDA-compatible GPU for ChromaDB acceleration

### Installation

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install llama-cpp-python with GPU support
pip install llama-cpp-python --no-binary llama-cpp-python --extra-index-url https://mlc.ai/wheels
```

### Running the Server

```bash
# Start the FastAPI server
uvicorn main:app --reload
```

The API will be available at http://localhost:8000/

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

Currently, all endpoints are stubbed with dummy data. The actual implementations will be added in the next phase.

### Adding a New Agent

1. Create a new agent class in `agents/` that inherits from `BaseAgent`
2. Implement the required methods (`run`, `stop`, `reflect`)
3. Register the agent in the API

### Adding a New Endpoint

1. Create a new router file in `api/`
2. Define the endpoint handlers and routes
3. Include the router in `api/__init__.py` 
