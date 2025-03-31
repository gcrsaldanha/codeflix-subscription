from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.application.create_plan import CreatePlanUseCase
from src.application.create_user_account import CreateUserAccountUseCase
from src.domain.repositories import PlanRepository, UserAccountRepository
from src.infra.auth import AuthService
from src.infra.db import (
    get_session,
    SQLModelPlanRepository,
    SQLModelUserAccountRepository,
)
from src.tests.fixtures.infra.repositories.in_memory_auth_service import (
    InMemoryAuthService,
)

# Database
SessionDep = Annotated[Session, Depends(get_session)]


# Repositories
def get_plan_repository(session: SessionDep) -> PlanRepository:
    return SQLModelPlanRepository(session)


def get_user_account_repository(session: SessionDep) -> UserAccountRepository:
    return SQLModelUserAccountRepository(session)


PlanRepositoryDep = Annotated[PlanRepository, Depends(get_plan_repository)]
UserAccountRepositoryDep = Annotated[
    UserAccountRepository, Depends(get_user_account_repository)
]


# External dependencies
def get_auth_service() -> AuthService:
    return InMemoryAuthService()  # TODO: replace by KeycloakAuthService


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


# Use cases
def get_create_plan_use_case(plan_repository: PlanRepositoryDep) -> CreatePlanUseCase:
    return CreatePlanUseCase(plan_repository)


def get_create_user_account_use_case(
    auth_service: AuthServiceDep,
    user_account_repository: UserAccountRepositoryDep,
) -> CreateUserAccountUseCase:
    return CreateUserAccountUseCase(auth_service, user_account_repository)


CreatePlanUseCaseDep = Annotated[CreatePlanUseCase, Depends(get_create_plan_use_case)]
CreateUserAccountUseCaseDep = Annotated[
    CreateUserAccountUseCase, Depends(get_create_user_account_use_case)
]
