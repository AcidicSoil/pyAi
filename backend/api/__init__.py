"""
filepath: backend/api/__init__.py
API package initialization and router collection.
"""

from fastapi import APIRouter

from .agents import router as agents_router

# Create main API router
api_router = APIRouter()

# Include all module routers
api_router.include_router(agents_router)

# TODO: Add additional routers as they are created
