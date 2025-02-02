from pydantic import BaseModel


class ValueObject(BaseModel):
    class Config:
        frozen = True
        validate_assignment = True
        extra = "forbid"
