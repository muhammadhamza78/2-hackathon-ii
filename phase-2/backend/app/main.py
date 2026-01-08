from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Correct imports based on your current structure
from app.api.v1 import auth, tasks, profile  # directly import auth.py, tasks.py, profile.py
from app.config import settings  # your settings




# -----------------------------
# Create FastAPI instance
# -----------------------------
app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="API for managing tasks, users, and profiles."
)

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


# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(profile.router, prefix="/api/v1", tags=["Profile"])


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
@app.get("/")
async def root():
    return {
        "message": "Task Management API",
        "version": "1.0.0",
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
