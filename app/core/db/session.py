# app/core/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import get_settings
from sqlalchemy.orm import declarative_base
import re

Base = declarative_base()
settings = get_settings()

# Ensure we use the asyncpg driver and handle SSL properly
db_url = settings.database_url
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove any existing sslmode parameter to avoid conflicts with connect_args
db_url = re.sub(r'\?sslmode=[^&]+', '', db_url)
db_url = re.sub(r'&sslmode=[^&]+', '', db_url)

engine = create_async_engine(
    db_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    # SSL is usually required for Supabase
    connect_args={"ssl": "require"} if "localhost" not in db_url else {}
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
