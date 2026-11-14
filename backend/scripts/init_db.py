"""Database table creation and migration helper."""
import asyncio
from app.database import Base, engine
from app.models import *  # noqa: F401, F403


async def init_tables():
    print("Creating all database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_tables())
