from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.application.ports.notification_service import NotificationService
from src.application.ports.payment_gateway import PaymentGateway
from src.domain.repositories import SubscriptionRepository


class RenewSubscriptionInput(BaseModel):
    subscription_id: UUID
    payment_token: str


class RenewSubscriptionOutput(BaseModel):
    subscription_id: UUID
    renewal_end_date: datetime


class RenewSubscriptionUseCase:
    def __init__(
        self,
        payment_gateway: PaymentGateway,
        subscription_repo: SubscriptionRepository,
        notification_service: NotificationService,
    ) -> None:
        self._payment_gateway = payment_gateway
        self._subscription_repo = subscription_repo
        self._notification_service = notification_service

    def execute(self, input: RenewSubscriptionInput) -> RenewSubscriptionOutput | None:
        subscription = self._subscription_repo.get_user_subscription(input.subscription_id)
        if not subscription:
            return None

        payment_result = self._payment_gateway.charge(
            amount=subscription.plan.price,
            token=input.payment_token
        )

        subscription.renew(payment_result)

        if not payment_result.success:
            self._notification_service.notify(
                user_id=subscription.user_id,
                message=payment_result.error_message,
            )

        self._subscription_repo.save(subscription)

        return RenewSubscriptionOutput(
            subscription_id=subscription.id,
            renewal_end_date=subscription.end_date,
        )
