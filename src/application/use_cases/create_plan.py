from uuid import UUID

from pydantic import BaseModel

from src.domain.entities import Plan
from src.domain.repositories import PlanRepository
from src.domain.value_objects import MonetaryValue


class CreatePlanInput(BaseModel):
    name: str
    price: MonetaryValue


class CreatePlanOutput(BaseModel):
    id: UUID
    name: str
    price: MonetaryValue


class DuplicatePlanError(Exception):
    pass


class CreatePlanUseCase:
    def __init__(self, plan_repository: PlanRepository):
        self._repo = plan_repository

    def execute(self, input: CreatePlanInput) -> CreatePlanOutput:
        existing = self._repo.find_by_name(input.name)
        if existing:
            raise DuplicatePlanError()

        plan = Plan(name=input.name, price=input.price)
        self._repo.save(plan)

        return CreatePlanOutput(
            id=plan.id,
            name=plan.name,
            price=plan.price,
        )
