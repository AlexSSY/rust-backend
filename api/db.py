from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from api.config import config


engine = create_async_engine(f"sqlite+aiosqlite:///{config.DB_NAME}", echo=True)
AsyncSessionLocal = sessionmaker(
    engine, autoflush=False, autocommit=False, class_=AsyncSession
)
Base = declarative_base()
