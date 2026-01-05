"""
FastAPI Application Entry Point
Main application configuration and startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, tasks
from app.db.session import init_db
from app.config import settings


app = FastAPI(
    title="Task Management API",
    description="Backend API for Task Management System with JWT Authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ✅ CORS (local + vercel)
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://2-hackathon-ii.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ SINGLE PREFIX SOURCE (HERE ONLY)
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])


@app.on_event("startup")
async def startup_event():
    if settings.DEBUG:
        init_db()


@app.get("/")
async def root():
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "auth": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login",
        },
    }


@app.get("/health")
async def health():
    from app.db.session import engine
    from sqlmodel import text

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        return {"status": "db_error"}
