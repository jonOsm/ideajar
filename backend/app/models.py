from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

class Pitch(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str
    type: str
    submitter: str = "Anonymous"

class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pitch_id: UUID
    vote_type: str
