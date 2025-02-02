from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.domain.events import DomainEvent


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    events: list[DomainEvent] = Field(default_factory=list)

    class Config:
        allow_mutation = True
        validate_assignment = True
        extra = "forbid"
