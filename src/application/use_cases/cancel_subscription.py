from uuid import UUID

from pydantic import BaseModel

from src.application.exceptions import SubscriptionNotFoundError
from src.domain.repositories import SubscriptionRepository


class CancelSubscriptionInput(BaseModel):
    user_subscription_id: UUID


class CancelSubscriptionUseCase:
    def __init__(self, subscription_repo: SubscriptionRepository):
        self._subscription_repo = subscription_repo

    def execute(self, input: CancelSubscriptionInput) -> None:
        subscription = self._subscription_repo.get_user_subscription(input.user_subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError()

        subscription.cancel()
        self._subscription_repo.save(subscription)
