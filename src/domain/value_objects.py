from decimal import Decimal
from enum import StrEnum, auto

from pydantic import Field

from src.domain.shared.value_object import ValueObject


class Currency(StrEnum):
    BRL = auto()
    USD = auto()


def check_currency(fn):
    def wrapper(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return fn(self, other)

    return wrapper


class MonetaryValue(ValueObject):
    amount: Decimal = Field(gt=0)
    currency: Currency = Currency.BRL

    @check_currency
    def __le__(self, other):
        return self.amount <= other.amount

    @check_currency
    def __lt__(self, other):
        return self.amount < other.amount

    @check_currency
    def __add__(self, other):
        return MonetaryValue(amount=self.amount + other.amount, currency=self.currency)

    @check_currency
    def __sub__(self, other):
        return MonetaryValue(amount=self.amount - other.amount, currency=self.currency)

    @check_currency
    def __mul__(self, other):
        return MonetaryValue(amount=self.amount * other.amount, currency=self.currency)

    @check_currency
    def __divmod__(self, other):
        return MonetaryValue(amount=self.amount / other.amount, currency=self.currency)

    @check_currency
    def __mod__(self, other):
        return MonetaryValue(amount=self.amount % other.amount, currency=self.currency)


class SubscriptionStatus(StrEnum):
    ACTIVE = auto()
    CANCELED = auto()


class BillingPeriod(StrEnum):
    MONTHLY = auto()
    ANNUAL = auto()


class UserRole(StrEnum):
    ADMIN = auto()
    USER = auto()


class BillingAddress(ValueObject):
    street: str
    city: str
    state: str
    zip_code: str
    country: str


class PaymentResult(ValueObject):
    success: bool
    message: str = ""
