# Phase 2 – Stub Out

## Objective
Establish a fully structured project skeleton that mirrors the architecture defined in `masterplan.md`. Stub files must be created with purpose comments, placeholder imports, and clearly marked TODOs. A **live frontend UI** must be operational during this phase to shorten debugging cycles and validate routing.

## Frontend Requirements
- Live development server using **Vite + React + TailwindCSS + shadcn/ui**
- Pages:
  - `/`: Agent Dashboard
  - `/agents/[id]`: Individual Agent View
  - `/memory`: Memory Browser
- Components:
  - `AgentCard`, `ChatPanel`, `MemoryItem`, `ToolSelector`
- Use Tailwind utility classes + shadcn design system
- Include placeholder routing and base layout shell

## Backend Requirements
- FastAPI with async routes
- Dummy endpoints:
  - `POST /research` – returns mock research payload
  - `GET /memory/{agent_id}` – returns static memory array
  - `POST /integrations/{tool}` – responds with mocked integration result

## Directory Structure
```
/ai-agent-framework
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |-- pages/
|   |   |-- lib/
|   |   |-- App.tsx
|   |   |-- main.tsx
|-- backend/
|   |-- api/
|   |-- agents/
|   |-- memory/
|   |-- orchestration/
|   |-- integrations/
|   |-- llm/
|   |-- main.py
|-- infra/
|   |-- Dockerfile
|   |-- terraform/
|-- README.md
```

## Stubbing Instructions
- All Python files should include:
  - Top comment with purpose
  - Filepath comment
  - Placeholder imports
  - Empty class/function declarations
  - `# TODO:` markers for future logic

- React files:
  - Components should return `div` with name label
  - Pages should include placeholder state + layout structure

## Deliverables
- Live frontend app served on localhost (via `npm run dev`)
- FastAPI backend that connects to frontend (no real logic yet)
- Codebase with clearly stubbed modules for:
  - LLM interface
  - Memory interface (ChromaDB)
  - Prefect orchestration
  - Slack + Notion integration modules
  - Core agent class definition (empty)

## Next Step
Once all modules are stubbed and the frontend + backend are running without fatal errors, move on to **Phase 3 – Fully Code Out** where production logic will be implemented inside this scaffold.

