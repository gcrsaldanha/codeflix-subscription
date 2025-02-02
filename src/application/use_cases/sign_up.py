from uuid import UUID

from pydantic import BaseModel, SecretStr, EmailStr

from src.application.ports import AuthService
from src.domain.entities import UserAccount
from src.domain.exceptions import UserAlreadyExistsError
from src.domain.repositories import UserRepository
from src.domain.value_objects import BillingAddress


class SignUpInput(BaseModel):
    email: EmailStr
    password: SecretStr
    billing_address: BillingAddress


class SignUpOutput(BaseModel):
    user_id: UUID
    iam_user_id: UUID


class SignUpUseCase:
    def __init__(
        self,
        auth_service: AuthService,
        user_repository: UserRepository,
    ) -> None:
        self._auth_service = auth_service
        self._user_repository = user_repository

    def execute(self, input: SignUpInput) -> SignUpOutput:
        if self._auth_service.find_by_email(input.email):
            raise UserAlreadyExistsError(f"User {input.email} already exists")

        # TODO: do we need to create user in Keycloak or we will handle the event FROM Keycloak?
        iam_user = self._auth_service.create_user(
            email=input.email,
            password=input.password.get_secret_value()
        )

        user = UserAccount(
            iam_user_id=iam_user.iam_user_id,
            email=input.email,
            billing_address=input.billing_address,
        )

        self._user_repository.save(user)

        return SignUpOutput(
            user_id=user.id,
            iam_user_id=iam_user.iam_user_id,
        )
