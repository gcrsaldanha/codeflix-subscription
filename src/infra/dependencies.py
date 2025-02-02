from typing import Generator

from sqlalchemy.orm import Session

from src.infra.adapters.email_service import EmailService, EmailServiceConfig
from src.infra.adapters.keycloak_adapter import KeycloakAuthService, KeycloakConfig
from src.infra.db.session import get_session


def get_auth_service():
    return KeycloakAuthService(config=KeycloakConfig())


def get_notification_service():
    return EmailService(config=EmailServiceConfig())


def get_db_session() -> Generator[Session]:
    return get_session()
