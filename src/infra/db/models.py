from datetime import datetime, UTC
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import JSON, Enum
from sqlmodel import SQLModel, Field

from src.domain.value_objects import SubscriptionStatus, Currency


class UserAccount(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    iam_user_id: str
    name: str
    email: str
    billing_address: str = Field(sa_column=Field(JSON))

    class Config:
        arbitrary_types_allowed = True


class Plan(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    price: Decimal
    currency: Currency = Field(sa_column=Field(Enum(Currency)))


class Subscription(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="useraccount.id")
    plan_id: UUID = Field(foreign_key="plan.id")
    start_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_date: datetime
    status: SubscriptionStatus = Field(sa_column=Field(Enum(SubscriptionStatus)))
    is_trial: bool = False
