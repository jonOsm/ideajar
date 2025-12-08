from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from fastapi_users import schemas

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)

class UserRead(schemas.BaseUser[UUID]):
    username: str

from pydantic import field_validator
from app.constants import MIN_PASSWORD_LENGTH

class UserCreate(schemas.BaseUserCreate):
    username: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        import re
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError('REGISTER_INVALID_USERNAME_FORMAT')
        if len(v) < 3 or len(v) > 20:
             raise ValueError('REGISTER_INVALID_USERNAME_LENGTH')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < MIN_PASSWORD_LENGTH:
            raise ValueError('REGISTER_INVALID_PASSWORD')
        return v

class UserUpdate(schemas.BaseUserUpdate):
    pass

class Pitch(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str
    type: str
    submitter: str = "Anonymous"

class PitchCreate(SQLModel):
    title: str
    description: str
    type: str

class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pitch_id: UUID
    vote_type: str
