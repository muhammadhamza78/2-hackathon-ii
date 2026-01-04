"""
FastAPI Application Entry Point
Main application configuration and startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, tasks
from app.db.session import init_db
from app.config import settings


# Create FastAPI application
app = FastAPI(
    title="Task Management API",
    description="Backend API for Task Management System with JWT Authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS
# Add local and deployed frontend URLs here
allowed_origins = [
    "http://localhost:3000",  # Local Next.js dev
    "https://2-hackathon-ii.vercel.app",  # Deployed frontend
    # If you have preview deployments in Vercel:
    "https://2-hackathon-ii-*.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])


@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on startup (development only).
    Use migrations (Alembic) for production.
    """
    if settings.DEBUG:
        init_db()


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    from app.db.session import engine
    from sqlmodel import text

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "disconnected"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
