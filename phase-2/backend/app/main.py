"""
FastAPI Application Entry Point
Main application configuration and startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, tasks
from app.db.session import init_db
from app.config import settings


# --------------------------------------------------
# Create FastAPI app
# --------------------------------------------------
app = FastAPI(
    title="Task Management API",
    description="Backend API for Task Management System with JWT Authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# --------------------------------------------------
# CORS Configuration (LOCAL + PRODUCTION)
# --------------------------------------------------
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    # ✅ Vercel production
    "https://2-hackathon-ii.vercel.app",

    # ✅ Vercel preview (explicit example — optional)
    "https://2-hackathon-ii-git-main.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Routers
# --------------------------------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])


# --------------------------------------------------
# Startup
# --------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables in development.
    """
    if settings.DEBUG:
        init_db()


# --------------------------------------------------
# Root
# --------------------------------------------------
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Task Management API is running 🚀",
        "docs": "/docs",
        "health": "/health",
        "auth": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login",
        },
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    from app.db.session import engine
    from sqlmodel import text

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "error", "database": "disconnected"}


# --------------------------------------------------
# Local run
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
