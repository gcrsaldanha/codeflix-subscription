from abc import ABC, abstractmethod
from uuid import UUID


class NotificationService(ABC):
    @abstractmethod
    def notify(self, user_id: UUID, message: str) -> None:
        pass
