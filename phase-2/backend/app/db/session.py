from sqlmodel import Session, create_engine
from typing import Generator
from app.config import settings


DATABASE_URL = settings.DATABASE_URL

# Fix: Convert postgres:// to postgresql:// (Railway/Heroku compatibility)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fix: Ensure SSL mode for Neon/production databases
if DATABASE_URL.startswith("postgresql://") and "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require" if "?" not in DATABASE_URL else "&sslmode=require"

engine_args = {
    "echo": settings.DEBUG,
    "pool_pre_ping": True,
}

# Apply pooling ONLY for non-SQLite databases
if not DATABASE_URL.startswith("sqlite"):
    engine_args.update({
        "pool_size": 10,
        "max_overflow": 0,
        "pool_timeout": 30,
        "pool_recycle": 3600,
    })

engine = create_engine(DATABASE_URL, **engine_args)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db() -> None:
    from sqlmodel import SQLModel
    from app.models.user import User
    from app.models.task import Task

    SQLModel.metadata.create_all(engine)
