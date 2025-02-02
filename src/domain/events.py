from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)


class UserSubscribedEvent(DomainEvent):  # Domain or application layer event?
    user_id: UUID
    plan_id: UUID


class PaymentFailedEvent(DomainEvent):  # Application layer event
    user_id: UUID
    plan_id: UUID
    error_message: str
