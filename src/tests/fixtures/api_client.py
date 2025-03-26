from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from src.infra.api.fastapi import app
from src.infra.db import get_session

_test_engine = create_engine("sqlite:///:memory:")


def _get_test_session() -> Iterator[Session]:
    SQLModel.metadata.create_all(_test_engine)
    with Session(_test_engine) as session:
        yield session


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides[get_session] = _get_test_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
