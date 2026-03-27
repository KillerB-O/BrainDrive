from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.scoring.router import router as scoring_router

app = FastAPI(title="BrainDrive API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    scoring_router,
    prefix="/api/v1/scoring",
    tags=["Scoring"]
)

@app.get("/")
async def root():
    return {"status": "running"}