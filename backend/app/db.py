import os
from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in web environment or .env file")

# Parse params if needed, but usually sqlalchemy handles URL params well.
# Note: provided URL had sslmode=require, we changed it to ssl=require in .env for asyncpg compatibility if needed,
# or we can pass connect_args={"ssl": "require"}

engine = create_async_engine(
    DATABASE_URL,
    echo=True, # Enable echo for debugging during dev
    future=True,
    pool_pre_ping=True,  # Check connection health before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # For reset
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
