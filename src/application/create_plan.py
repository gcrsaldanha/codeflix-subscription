from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import DuplicatePlanError
from src.domain.plan import Plan
from src.domain.value_objects import MonetaryValue


class CreatePlanInput(BaseModel):
    name: str
    price: MonetaryValue


class CreatePlanOutput(BaseModel):
    id: UUID
    name: str
    price: MonetaryValue


class CreatePlanUseCase:
    def __init__(self, repository) -> None:
        self._repo = repository

    def execute(self, input: CreatePlanInput) -> CreatePlanOutput:
        existing = self._repo.find_by_name(input.name)
        if existing:
            raise DuplicatePlanError("Plan with this name already exists")

        plan = Plan(name=input.name, price=input.price)
        self._repo.save(plan)

        return CreatePlanOutput(
            id=plan.id,
            name=plan.name,
            price=plan.price,
        )
