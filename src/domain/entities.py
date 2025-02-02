from datetime import datetime, UTC
from typing import ClassVar
from uuid import UUID

from dateutil.relativedelta import relativedelta
from pydantic import EmailStr, Field

from src.domain.exceptions import RenewSubscriptionError, UpgradeSubscriptionError
from src.domain.shared.entity import Entity
from src.domain.value_objects import MonetaryValue, SubscriptionStatus, BillingAddress, PaymentResult


class UserAccount(Entity):
    iam_user_id: str
    name: str
    email: EmailStr
    billing_address: BillingAddress


class Plan(Entity):
    name: str
    price: MonetaryValue


class Subscription(Entity):
    user_id: UUID
    plan_id: UUID
    start_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_date: datetime
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    is_trial: bool = False

    TRIAL_DURATION: ClassVar[int] = 7

    # TODO: validate end_date > start_date
    @classmethod
    def create_trial(cls, user_id: UUID, plan_id: UUID) -> "Subscription":
        now = datetime.now(UTC)
        return cls(
            user_id=user_id,
            plan_id=plan_id,
            start_date=now,
            end_date=now + relativedelta(days=cls.TRIAL_DURATION),
            status=SubscriptionStatus.ACTIVE,
            is_trial=True,
        )

    @classmethod
    def create_regular(cls, user_id: UUID, plan_id: UUID) -> "Subscription":
        now = datetime.now(UTC)
        return cls(
            user_id=user_id,
            plan_id=plan_id,
            start_date=now,
            end_date=now + relativedelta(months=1),
            status=SubscriptionStatus.ACTIVE,
            is_trial=False,
        )

    def renew(self, payment_result: PaymentResult) -> None:
        if self.is_canceled:
            raise RenewSubscriptionError("Cannot renew a canceled subscription")

        # TODO: reduce if/else -- extract to more methods
        if self.is_trial:
            if payment_result.success:
                self.upgrade()
            else:
                self.cancel()
        else:
            if payment_result.success:
                self.extend()
            else:
                self.convert_to_trial()

    def cancel(self):
        self.is_trial = False
        self.status = SubscriptionStatus.CANCELED
        self.end_date = datetime.now(UTC)

    def upgrade(self):
        if not self.is_trial:
            raise UpgradeSubscriptionError("Cannot upgrade a non-trial subscription")

        self.is_trial = False
        self.start_date = datetime.now(UTC)
        self.end_date = self.start_date + relativedelta(months=1)
        self.status = SubscriptionStatus.ACTIVE

    def extend(self):
        self.end_date += relativedelta(months=1)

    def convert_to_trial(self):
        self.is_trial = True
        self.start_date = datetime.now(UTC)
        self.end_date = self.start_date + relativedelta(days=self.TRIAL_DURATION)
        self.status = SubscriptionStatus.ACTIVE

    @property
    def is_active(self):
        return self.status == SubscriptionStatus.ACTIVE

    @property
    def is_canceled(self):
        return self.status == SubscriptionStatus.CANCELED

    @property
    def is_expired(self):
        return self.status == SubscriptionStatus.ACTIVE and self.end_date < datetime.now(UTC)
