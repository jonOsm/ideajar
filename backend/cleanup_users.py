import asyncio
from app.db import engine
from app.models import User
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def cleanup():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username.contains(" ")))
        users = result.scalars().all()
        for user in users:
            print(f"Deleting user: {user.username}")
            await session.delete(user)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(cleanup())
