# app/core/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import get_settings
from sqlalchemy.orm import declarative_base

Base = declarative_base()
settings = get_settings()


db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
db_url = db_url.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(
    db_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={"ssl": "require"}  # IMPORTANT for Supabase
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session