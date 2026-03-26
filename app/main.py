from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.db.session import engine, Base
import app.core.db.schema  # Ensure schema is loaded for creation
from app.modules.scoring.router import router as scoring_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Shared DB creation - The point of contact for all modules
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="BrainDrive Modular Monolith",
    version="1.0.0",
    lifespan=lifespan
)

# Mounting Modules
app.include_router(scoring_router, prefix="/api/v1/scoring", tags=["Scoring"])

@app.get("/")
async def root():
    return {"status": "BrainDrive Core Online", "architecture": "Modular Monolith"}
