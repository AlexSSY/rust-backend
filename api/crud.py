from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models import User


async def get_user_by_username(session: Session, *, username: str) -> Optional[User]:
    return session.scalar(select(User).where(User.username == username))
