#!/bin/bash
# Development script to run both frontend and backend

# Function to handle exit
cleanup() {
    echo "Shutting down servers..."
    kill $FRONTEND_PID $BACKEND_PID 2>/dev/null
    exit 0
}

# Set up trap for clean exit
trap cleanup SIGINT SIGTERM

# Check if servers are already running
echo "Checking for existing servers..."
FRONTEND_RUNNING=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 || echo "000")
BACKEND_RUNNING=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")

if [ "$FRONTEND_RUNNING" != "000" ]; then
    echo "Frontend is already running on http://localhost:5173"
else
    # Start frontend
    echo "Starting frontend (Vite)..."
    cd frontend && npm run dev &
    FRONTEND_PID=$!
    echo "Frontend process started with PID: $FRONTEND_PID"
    # Return to root directory
    cd ..
fi

# Wait a moment to allow frontend to start
sleep 2

if [ "$BACKEND_RUNNING" = "200" ]; then
    echo "Backend is already running on http://localhost:8000"
else
    # Start backend from project root
    echo "Starting backend (FastAPI)..."
    source backend/.venv/Scripts/activate && python -m uvicorn backend.main:app --reload --port 8000 &
    BACKEND_PID=$!
    echo "Backend process started with PID: $BACKEND_PID"
    # No need to cd .. as we are already in the root
fi

echo "Servers should be available at:"
echo "- Frontend: http://localhost:5173"
echo "- Backend: http://localhost:8000"
echo "Press Ctrl+C to stop both servers"

# Wait for processes if we started them
if [ -n "$FRONTEND_PID" ] || [ -n "$BACKEND_PID" ]; then
    wait $FRONTEND_PID $BACKEND_PID
else
    echo "No servers were started. Both may already be running."
    exit 0
fi
