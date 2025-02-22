import pytest

from src.application.create_plan import CreatePlanUseCase, CreatePlanInput
from src.application.exceptions import DuplicatePlanError
from src.domain.plan import Plan
from src.domain.value_objects import MonetaryValue, Currency
from src.tests.infra.in_memory_plan_repository import InMemoryPlanRepository


class TestCreatePlan:
    def test_when_plan_with_name_exists_then_return_error(self):
        plan = Plan(name="Basic", price=MonetaryValue(amount=100, currency=Currency.BRL))
        plan_repo = InMemoryPlanRepository(plans=[plan])

        use_case = CreatePlanUseCase(repository=plan_repo)

        with pytest.raises(DuplicatePlanError):
            use_case.execute(input=CreatePlanInput(
                name="Basi",
                price=MonetaryValue(amount=100, currency=Currency.BRL),
            ))

    def test_when_plan_with_name_does_not_exist_then_create_plan(self):
        plan_repo = InMemoryPlanRepository(plans=[])
        use_case = CreatePlanUseCase(repository=plan_repo)

        output = use_case.execute(input=CreatePlanInput(
            name="Basic",
            price=MonetaryValue(amount=100, currency=Currency.BRL),
        ))

        assert output.id is not None
        assert output.name == "Basic"
        assert output.price == MonetaryValue(amount=100, currency=Currency.BRL)

        assert len(plan_repo.plans) == 1
        assert output.id == plan_repo.find_by_name("Basic").id
