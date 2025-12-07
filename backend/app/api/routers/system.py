import os
from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import Pitch

router = APIRouter(tags=["System"])

@router.get("/health", operation_id="health_check")
async def health(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(select(1))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "ok", "environment": os.getenv("ENV", "dev"), "database": db_status}

@router.post("/seed")
async def seed_data(session: AsyncSession = Depends(get_session)):
    """Seed initial data."""
    result = await session.execute(select(Pitch))
    if result.scalars().first():
        return {"message": "Already seeded"}
    
    pitches = [
        Pitch(title="Cat Café & Laundromat", description="Drink coffee and pet cats while waiting for your laundry.", type="idea", submitter="Alice"),
        Pitch(title="Pineapple on Pizza is Good", description="The sweetness cuts the saltiness. Ideally with jalapeños.", type="opinion", submitter="Bob"),
    ]
    for p in pitches:
        session.add(p)
    await session.commit()
    return {"message": "Seeded 3 pitches"}
