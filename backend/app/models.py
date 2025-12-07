from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from fastapi_users import schemas

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)

class UserRead(schemas.BaseUser[UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

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
