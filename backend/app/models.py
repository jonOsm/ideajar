from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

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
