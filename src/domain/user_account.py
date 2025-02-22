from pydantic import EmailStr

from entity import Entity
from value_objects import ValueObject


class Address(ValueObject):
    street: str
    city: str
    state: str
    zip_code: str
    country: str


class UserAccount(Entity):
    iam_user_id: str
    name: str
    email: EmailStr
    billing_address: Address
