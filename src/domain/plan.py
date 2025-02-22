from entity import Entity
from value_objects import MonetaryValue


class Plan(Entity):
    name: str
    price: MonetaryValue
