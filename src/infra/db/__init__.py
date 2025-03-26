from sqlmodel import Session, SQLModel, create_engine

from .repositories.sql_model_plan_repository import SQLModelPlanRepository

DATABASE_URL = "sqlite:///./subscription_service.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


__all__ = [
    "SQLModelPlanRepository",
    "create_db_and_tables",
    "get_session",
]
