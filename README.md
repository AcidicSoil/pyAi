<!-- @format -->

# Modular AI Agent System

A Pythonic, GPU-accelerated, local-first AI research agent framework.

## Project Overview

This system provides a modular framework for AI agents that can perform various tasks, including research, code generation, and data analysis. It is designed to be:

- **Local-first**: Run models locally with GPU acceleration
- **Modular**: Easily add new agents and capabilities
- **Extensible**: Integrate with external services and APIs
- **Collaborative**: Agents can work together to solve complex problems

## Architecture

The system consists of two main components:

1. **Frontend**: Vite + React + TypeScript + TailwindCSS
2. **Backend**: FastAPI + Pydantic + Prefect + LLM integrations

## Getting Started

### Prerequisites

- Node.js 16+ and npm/yarn for frontend
- Python 3.11+ for backend
- Vulkan-compatible GPU for LLM acceleration

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-agent-framework.git
cd ai-agent-framework

# Install frontend dependencies
cd frontend
npm install
cd ..

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### Running in Development Mode

```bash
# Run both frontend and backend
./run-dev.sh
```

This will start:
- Frontend at http://localhost:5173/
- Backend at http://localhost:8000/

## Project Structure

```
/ai-agent-framework
├── frontend/           # Vite + React frontend
├── backend/            # FastAPI backend
│   ├── agents/         # Agent implementations
│   ├── api/            # API endpoints
│   ├── llm/            # LLM interfaces
│   ├── memory/         # Memory systems
│   ├── orchestration/  # Prefect workflows
│   └── integrations/   # External service integrations
└── infra/              # Deployment and infrastructure
```

## Current Status

The project is currently in the **stubout** phase, with basic frontend and backend stubs implemented. The next step is to implement the full functionality in the **fullycode** phase.

---

## 🚀 Overview

This framework is designed to:

- Run modular autonomous agents using `llama.cpp` inference
- Coordinate multi-agent workflows with Prefect
- Store and retrieve knowledge via ChromaDB (with cloud sync)
- Integrate seamlessly with tools like Slack, Notion, GitHub
- Support local and AWS G5 deployment with one Dockerfile

---

## 🧠 Key Features

- **Agent Reflection Loops** – Agents self-improve based on past outputs
- **Vulkan-Accelerated LLMs** – Powered by `unsloth/gemma-3-4b-it` or `mistral-7b`
- **Shared + Isolated Memory** – ChromaDB memory partitions with S3 sync
- **FastAPI + Async Architecture** – API endpoints for research, memory, and integrations
- **Pluggable Integrations** – Slack, Notion, GitHub, Jira (modular)
- **Frontend Dashboard** – Vite + React + Tailwind + shadcn/ui for live UI feedback

---

## 🧱 Tech Stack

| Layer         | Stack                                          |
| ------------- | ---------------------------------------------- |
| LLM Backend   | llama.cpp + Vulkan + quantized models          |
| Agents        | Python classes w/ reasoning, reflection, tools |
| Orchestration | Prefect 2.x                                    |
| API Layer     | FastAPI, Pydantic v2                           |
| Memory        | ChromaDB (local), S3 sync, Pinecone optional   |
| Frontend      | Vite + React + TailwindCSS + shadcn/ui         |
| Deployment    | Docker (local/cloud), Terraform (AWS G5)       |

---

## 📂 Project Structure

```bash
/ai-agent-framework
├── frontend/                # Live UI powered by Vite/React
├── backend/                 # Python modules
│   ├── api/                 # FastAPI endpoints
│   ├── agents/              # Agent class definitions
│   ├── llm/                 # Inference wrappers (llama.cpp)
│   ├── memory/              # ChromaDB abstraction
│   ├── orchestration/       # Prefect flows
│   ├── integrations/        # Slack, Notion, etc.
│   └── main.py              # FastAPI entrypoint
├── infra/                   # Dockerfile + Terraform config
│   └── terraform/
├── .cursorrules             # Project-wide Cursor rules
├── README.md                # You are here
```

---

## 🧪 Dev Workflow

1. **Phase 1**: [`masterplan.md`](./masterplan.md) – Plan architecture and flows
2. **Phase 2**: [`stubout.md`](./stubout.md) – Create stubbed files + live frontend
3. **Phase 3**: [`fullycode.md`](./fullycode.md) – Build production-ready system

> 📌 Frontend must always run before implementing backend logic

---

## 🛠 Setup Instructions

```bash
# Clone repo and enter project
$ git clone https://github.com/your-org/ai-agent-framework
$ cd ai-agent-framework

# Start frontend
$ cd frontend && npm install && npm run dev

# In new terminal, setup Python backend
$ cd backend && python3 -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt
$ uvicorn main:app --reload
```

---

## 📡 API Endpoints (WIP)

- `POST /research` – Start research workflow
- `GET /memory/{agent_id}` – Fetch memory snapshots
- `POST /integrations/{tool}` – Trigger integration handlers

---

## 📋 Todo / Status

- [x] Define architecture
- [x] Create dev rules + Cursor-compatible .mdc files
- [ ] Stub frontend + backend
- [ ] Build and test agent logic
- [ ] Integration modules (Slack, Notion, etc.)
- [ ] Prefect flows for reasoning and orchestration

---

## 🔐 License

MIT © 2025 — Built for open collaboration
