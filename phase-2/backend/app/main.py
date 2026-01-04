"""
FastAPI Application Entry Point
Main application configuration and startup.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, tasks
from app.db.session import init_db
from app.config import settings

# --------------------------
# Environment
# --------------------------
IS_DEV = settings.DEBUG

# --------------------------
# App Init
# --------------------------
app = FastAPI(
    title="Task Management API",
    description="Backend API for Task Management System with JWT Authentication",
    version="1.0.0",
    docs_url="/docs" if IS_DEV else None,
    redoc_url="/redoc" if IS_DEV else None,
)

# --------------------------
# CORS Middleware
# --------------------------
# Railway/Vercel provides env vars as STRING
if isinstance(settings.CORS_ORIGINS, str):
    allowed_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
else:
    allowed_origins = settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Routers
# --------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])

# --------------------------
# Startup Event
# --------------------------
@app.on_event("startup")
async def startup_event():
    if IS_DEV:
        # Initialize DB in dev only (use Alembic in prod)
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
            "login": "POST /api/auth/login",
            "tasks": "GET/POST /api/tasks"
        },
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
# Local Run
# --------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=IS_DEV
    )
