from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import UserAccount, Subscription, Plan


class PlanRepository(ABC):
    @abstractmethod
    def find_by_id(self, plan_id: UUID) -> Plan:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Plan:
        pass

    @abstractmethod
    def save(self, plan: Plan) -> None:
        pass


class SubscriptionRepository(ABC):
    @abstractmethod
    def get_user_subscription(self, user_id: UUID) -> Subscription:
        pass

    @abstractmethod
    def save(self, subscription: Subscription) -> None:
        pass


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: UserAccount) -> None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> UserAccount: ...
