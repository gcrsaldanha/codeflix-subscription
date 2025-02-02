from abc import ABC, abstractmethod

from src.domain.value_objects import MonetaryValue, PaymentResult


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: MonetaryValue, token: str) -> PaymentResult:
        pass
