from fastapi import Depends
from sqlalchemy.orm import Session

from api.db import SessionLocal


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


session_dep: Session = Depends(get_session)
