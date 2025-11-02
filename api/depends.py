from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import AsyncSessionLocal


async def get_session():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


session_dep: AsyncSession = Depends(get_session)
