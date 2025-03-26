from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.application.create_plan import CreatePlanUseCase
from src.domain.repositories import PlanRepository
from src.infra.db import get_session, SQLModelPlanRepository

SessionDep = Annotated[Session, Depends(get_session)]


def get_plan_repository(session: SessionDep) -> PlanRepository:
    return SQLModelPlanRepository(session)


PlanRepositoryDep = Annotated[PlanRepository, Depends(get_plan_repository)]


def get_create_plan_use_case(plan_repository: PlanRepositoryDep) -> CreatePlanUseCase:
    return CreatePlanUseCase(plan_repository)


CreatePlanUseCaseDep = Annotated[CreatePlanUseCase, Depends(get_create_plan_use_case)]
