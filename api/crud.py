from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User


async def get_user_by_username(session: AsyncSession, *, username: str) -> Optional[User]:
    return await session.scalar(
        select(User).where(User.username == username)
    )


async def store_new_user(session: AsyncSession, *, username: str, password_digest: str) -> bool:
    new_user = User(
        username=username,
        password_digest=password_digest
    )

    try:
        session.add(new_user)
        await session.commit()
    except Exception:
        return False
    return True
