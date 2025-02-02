from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import (
    PlanNotFoundError,
    UserNotFoundError,
)
from src.application.ports.auth_service import AuthService
from src.application.ports.notification_service import NotificationService
from src.application.ports.payment_gateway import PaymentGateway
from src.domain.entities import Subscription
from src.domain.exceptions import SubscriptionConflictError
from src.domain.repositories import PlanRepository, SubscriptionRepository


class SubscribeToPlanInput(BaseModel):
    user_id: UUID
    plan_id: UUID
    payment_token: str


class SubscribeToPlanOutput(BaseModel):
    subscription_id: UUID
    subscription_tier: str
    subscription_start_date: datetime
    subscription_end_date: datetime
    is_trial: bool


class SubscribeToPlanUseCase:
    def __init__(
        self,
        auth_service: AuthService,
        payment_gateway: PaymentGateway,
        plan_repository: PlanRepository,
        subscription_repository: SubscriptionRepository,
        notification_service: NotificationService,
    ) -> None:
        self._auth_service = auth_service
        self._payment_gateway = payment_gateway
        self._plan_repo = plan_repository
        self._subscription_repo = subscription_repository
        self._notification_service = notification_service

    def execute(self, input: SubscribeToPlanInput) -> SubscribeToPlanOutput:
        if not self._auth_service.find_user_by_id(input.user_id):
            raise UserNotFoundError("User does not exist")

        plan = self._plan_repo.find_by_id(input.plan_id)
        if not plan:
            raise PlanNotFoundError(f"Plan {input.plan_id} not found")

        current_subscription = self._subscription_repo.get_user_subscription(input.user_id)
        if current_subscription and current_subscription.is_active:
            raise SubscriptionConflictError("User already has an active subscription")

        payment_result = self._payment_gateway.charge(amount=plan.price, token=input.payment_token)

        if payment_result.success:
            subscription = Subscription.create_regular(user_id=input.user_id, plan_id=plan.id)
        else:
            self._notification_service.notify(user_id=input.user_id, message="Payment failed")
            subscription = Subscription.create_trial(user_id=input.user_id, plan_id=plan.id)

        self._subscription_repo.save(subscription)
        return SubscribeToPlanOutput(
            subscription_id=subscription.id,
            subscription_tier=plan.name,
            subscription_start_date=subscription.start_date,
            subscription_end_date=subscription.end_date,
            is_trial=subscription.is_trial,
        )
