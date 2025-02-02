from typing import Dict, Optional
from uuid import UUID

from src.domain.entities import UserAccount, Plan, Subscription
from src.domain.repositories import UserRepository, PlanRepository, SubscriptionRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: Dict[UUID, UserAccount] = {}

    def save(self, user: UserAccount) -> None:
        self._users[user.id] = user

    def find_by_id(self, user_id: UUID) -> Optional[UserAccount]:
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[UserAccount]:
        return next((u for u in self._users.values() if u.email == email), None)


class InMemoryPlanRepository(PlanRepository):
    def __init__(self):
        self._plans: Dict[UUID, Plan] = {}

    def save(self, plan: Plan) -> None:
        self._plans[plan.id] = plan

    def find_by_id(self, plan_id: UUID) -> Optional[Plan]:
        return self._plans.get(plan_id)

    def find_by_name(self, name: str) -> Optional[Plan]:
        return next((p for p in self._plans.values() if p.name == name), None)


class InMemorySubscriptionRepository(SubscriptionRepository):
    def __init__(self):
        self._subscriptions: Dict[UUID, Subscription] = {}
        self._user_subscriptions: Dict[UUID, UUID] = {}  # user_id -> subscription_id

    def save(self, subscription: Subscription) -> None:
        self._subscriptions[subscription.id] = subscription
        self._user_subscriptions[subscription.user_id] = subscription.id

    def find_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        return self._subscriptions.get(subscription_id)

    def get_user_subscription(self, user_id: UUID) -> Optional[Subscription]:
        sub_id = self._user_subscriptions.get(user_id)
        return self._subscriptions.get(sub_id) if sub_id else None
