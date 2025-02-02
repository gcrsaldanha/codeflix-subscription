from typing import Generator

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel


class SqlAlchemyConfig(BaseSettings):
    DATABASE_URL: str = "sqlite:///database.db"


engine = create_engine(SqlAlchemyConfig().DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
