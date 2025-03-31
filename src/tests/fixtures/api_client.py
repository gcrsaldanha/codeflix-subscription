from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from src.infra.api.dependencies import get_auth_service
from src.infra.api.fastapi import app
from src.infra.db import get_session
from src.tests.fixtures.infra.repositories.in_memory_auth_service import InMemoryAuthService

_test_engine = create_engine("sqlite:///:memory:")


def _get_test_session() -> Iterator[Session]:
    SQLModel.metadata.create_all(_test_engine)
    with Session(_test_engine) as session:
        yield session


@pytest.fixture(scope="function")
def client() -> Iterator[TestClient]:
    _auth_service = InMemoryAuthService()  # To ensure it's persistent for each test

    app.dependency_overrides[get_session] = _get_test_session
    app.dependency_overrides[get_auth_service] = lambda: _auth_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
