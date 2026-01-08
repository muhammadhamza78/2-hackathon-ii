from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Correct imports
from app.api.v1 import auth, tasks, profile
from app.db.session import init_db, engine
from app.config import settings
from sqlmodel import text

# -----------------------------
# Create FastAPI instance
# -----------------------------
app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="API for managing tasks, users, and profiles.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# -----------------------------
# CORS Configuration
# -----------------------------
# Always allow local development + production origins
default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

# Merge with environment variable origins
env_origins = settings.cors_origins_list() if hasattr(settings, 'cors_origins_list') else []
allowed_origins = list(set(default_origins + env_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(profile.router, prefix="/api/v1", tags=["Profile"])

# -----------------------------
# Startup Event
# -----------------------------
@app.on_event("startup")
async def startup_event():
    if settings.DEBUG:
        init_db()

# -----------------------------
# Root Route
# -----------------------------
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

# -----------------------------
# Health Check Route
# -----------------------------
@app.get("/health")
async def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        return {"status": "db_error"}
