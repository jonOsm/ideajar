from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import Pitch, Vote

router = APIRouter(tags=["Pitches"])

@router.get("/pitches", response_model=List[Pitch], operation_id="get_pitches")
async def get_pitches(session: AsyncSession = Depends(get_session)) -> List[Pitch]:
    """Get a list of pitches to swipe on."""
    # Logic: Get all pitches. In a real app, might filter by what user hasn't voted on.
    statement = select(Pitch)
    result = await session.execute(statement)
    return result.scalars().all()

@router.post("/vote", operation_id="submit_vote")
async def submit_vote(vote: Vote, session: AsyncSession = Depends(get_session)):
    """Submit a swipe vote."""
    session.add(vote)
    await session.commit()
    await session.refresh(vote)
    return {"status": "recorded", "vote": vote}
