"""
FastAPI Application Entry Point
Main application configuration and startup.

Spec Reference: specs/architecture.md (Backend section)
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, tasks
from app.db.session import init_db
from app.config import settings

# Determine if running in development
IS_DEV = settings.DEBUG

# Create FastAPI app
app = FastAPI(
    title="Task Management API",
    description="Backend API for Task Management System with JWT Authentication",
    version="1.0.0",
    docs_url="/docs" if IS_DEV else None,   # Only enable Swagger in dev
    redoc_url="/redoc" if IS_DEV else None
)

# --------------------------
# CORS Configuration
# --------------------------
# Read allowed origins from environment variable
# Format: CORS_ORIGINS=https://frontend1.app,https://frontend2.app
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
allowed_origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Include API Routers
# --------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])

# --------------------------
# Startup Event
# --------------------------
@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables (development only).
    In production, use Alembic migrations instead.
    """
    if IS_DEV:
        init_db()

# --------------------------
# Root Endpoint
# --------------------------
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs" if IS_DEV else None,
        "endpoints": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login"
        }
    }

# --------------------------
# Health Check
# --------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    from app.db.session import engine
    from sqlmodel import text

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "disconnected"}

# --------------------------
# Run Uvicorn
# --------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=IS_DEV
    )
