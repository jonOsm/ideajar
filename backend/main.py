import os
from contextlib import asynccontextmanager
from typing import List, Optional, Literal
from uuid import UUID, uuid4

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import SQLModel, Field, select
from sqlalchemy.ext.asyncio import AsyncSession

from db import init_db, get_session, engine

# --- Models ---
class Pitch(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str
    type: str # Literal not fully supported in SQLModel fields as logic constraint yet without Enum, using str for now
    submitter: str = "Anonymous"

class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pitch_id: UUID
    vote_type: str # "like" or "dislike"

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Retrieve/Check connection on startup
    # We could also create tables here if not using Alembic: await init_db()
    yield
    # Clean up DB connections on shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# --- API Routes ---

@app.get("/api/health", operation_id="health_check", tags=["System"])
async def health(session: AsyncSession = Depends(get_session)):
    try:
        # Simple query to check DB connection
        await session.execute(select(1))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "ok", "environment": os.getenv("ENV", "dev"), "database": db_status}

@app.get("/api/pitches", response_model=List[Pitch], operation_id="get_pitches", tags=["Pitches"])
async def get_pitches(session: AsyncSession = Depends(get_session)) -> List[Pitch]:
    """Get a list of pitches to swipe on."""
    # Logic: Get all pitches. In a real app, might filter by what user hasn't voted on.
    statement = select(Pitch)
    result = await session.execute(statement)
    return result.scalars().all()

@app.post("/api/vote", operation_id="submit_vote", tags=["Pitches"])
async def submit_vote(vote: Vote, session: AsyncSession = Depends(get_session)):
    """Submit a swipe vote."""
    session.add(vote)
    await session.commit()
    await session.refresh(vote)
    return {"status": "recorded", "vote": vote}

# --- Seed Endpoint (Temporary) ---
@app.post("/api/seed", tags=["System"])
async def seed_data(session: AsyncSession = Depends(get_session)):
    """Seed initial data."""
    # Check if empty
    result = await session.execute(select(Pitch))
    if result.scalars().first():
        return {"message": "Already seeded"}
    
    pitches = [
        Pitch(title="Cat Café & Laundromat", description="Drink coffee and pet cats while waiting for your laundry.", type="idea", submitter="Alice"),
        Pitch(title="Pineapple on Pizza is Good", description="The sweetness cuts the saltiness. Ideally with jalapeños.", type="opinion", submitter="Bob"),
        Pitch(title="Uber for Dog Walking", description="On-demand dog walkers nearby. GPS tracked.", type="pitch", submitter="Charlie"),
    ]
    for p in pitches:
        session.add(p)
    await session.commit()
    return {"message": "Seeded 3 pitches"}

# --- Static Assets (Production Only) ---
if os.path.exists("/app/frontend/dist"):
    app.mount("/assets", StaticFiles(directory="/app/frontend/dist/assets"), name="assets")

# --- SPA Fallback (Production Only) ---
@app.get("/{full_path:path}")
async def serve_vue_app(full_path: str):
    if full_path.startswith("api"):
        return {"error": "Not Found"}, 404
    
    if os.path.exists("/app/frontend/dist/index.html"):
        return FileResponse("/app/frontend/dist/index.html")
    
    return {"message": "Run 'npm run dev' to see the frontend"}