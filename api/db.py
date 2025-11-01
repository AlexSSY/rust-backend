from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from api.config import config


engine = create_engine(f'sqlite:///{config.DB_NAME}', connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)
Base = declarative_base()
