<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Correct imports based on your current structure
from app.api.v1 import auth, tasks, profile  # directly import auth.py, tasks.py, profile.py
from app.config import settings  # your settings




# -----------------------------
# Create FastAPI instance
# -----------------------------
=======
"""
FastAPI Application Entry Point
Main application configuration and startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, tasks
from app.db.session import init_db
from app.config import settings


>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
app = FastAPI(
    title="Task Management API",
    version="1.0.0",
<<<<<<< HEAD
    description="API for managing tasks, users, and profiles."
)

=======
    docs_url="/docs",
    redoc_url="/redoc",
)


# ✅ CORS (local + vercel)
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://2-hackathon-ii.vercel.app",
]

>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


<<<<<<< HEAD
# -----------------------------
# Include Routers
# -----------------------------
=======
# ✅ SINGLE PREFIX SOURCE (HERE ONLY)
>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(profile.router, prefix="/api/v1", tags=["Profile"])


<<<<<<< HEAD
# -----------------------------
# Startup Event
# -----------------------------
# @app.on_event("startup")
# async def startup_event():
#     if settings.DEBUG:
#         pass

# -----------------------------
# Routes
# -----------------------------
=======
@app.on_event("startup")
async def startup_event():
    if settings.DEBUG:
        init_db()


>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
@app.get("/")
async def root():
    return {
        "message": "Task Management API",
        "version": "1.0.0",
<<<<<<< HEAD
    }






=======
        "auth": {
            "register": "POST /api/auth/register",
            "login": "POST /api/auth/login",
        },
    }


>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
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
