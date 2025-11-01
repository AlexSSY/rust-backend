from typing import Optional
from sqlalchemy import ForeignKey, String, Engine
from sqlalchemy.orm import Mapped, mapped_column

from api.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    password_digest: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    provider: Mapped[str] = mapped_column(String(50))
    provider_user_id: Mapped[str] = mapped_column(String(100))
    access_token: Mapped[Optional[str]] = mapped_column(String(255))


def create_all(engine: Engine) -> None:
    Base.metadata.create_all(engine)
