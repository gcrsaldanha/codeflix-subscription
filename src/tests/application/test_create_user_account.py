import pytest

from src.application.create_plan import CreatePlanUseCase, CreatePlanInput
from src.application.create_user_account import CreateUserAccountInput, CreateUserAccountUseCase
from src.application.exceptions import DuplicatePlanError, UserAlreadyExistsError
from src.domain.plan import Plan
from src.domain.user_account import Address
from src.domain.value_objects import MonetaryValue, Currency
from src.tests.infra.in_memory_auth_service import InMemoryAuthService
from src.tests.infra.in_memory_plan_repository import InMemoryPlanRepository
from src.tests.infra.in_memory_user_account_repository import InMemoryUserAccountRepository


class TestCreatePlan:
    def test_when_email_is_registered_in_auth_service_then_raise_error(self):
        input = CreateUserAccountInput(
            name="John Doe",
            email="john@doe.com",
            password="secret",
            billing_address=Address(
                street="123 Main St",
                city="Anytown",
                state="NY",
                zip_code="12345",
                country="USA"
            )
        )
        auth_service = InMemoryAuthService(users=[input.email])
        use_case = CreateUserAccountUseCase(
            auth_service=auth_service,
            user_repository=None,
        )

        with pytest.raises(UserAlreadyExistsError):
            use_case.execute(input)

    def test_when_user_does_not_exist_then_create_user_account(self):
        input = CreateUserAccountInput(
            name="John Doe",
            email="john@doe.com",
            password="secret",
            billing_address=Address(
                street="123 Main St",
                city="Anytown",
                state="NY",
                zip_code="12345",
                country="USA"
            )
        )

        auth_service = InMemoryAuthService(users=[])
        account_repository = InMemoryUserAccountRepository(user_accounts=[])
        use_case = CreateUserAccountUseCase(
            auth_service=auth_service,
            user_repository=account_repository,
        )

        output = use_case.execute(input)

        assert output.user_id is not None
        assert output.iam_user_id is not None

        assert len(account_repository.user_accounts) == 1
        assert len(auth_service.users) == 1  # auth_service.create_user.assert_called_once_with(...)
