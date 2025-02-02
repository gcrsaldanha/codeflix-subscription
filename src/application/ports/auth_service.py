from abc import ABC, abstractmethod

from pydantic import BaseModel


class IAMError(Exception):
    pass


class IAMUser(BaseModel):
    iam_user_id: str
    email: str


class AuthService(ABC):
    @abstractmethod
    def create_user(self, email: str, password: str) -> IAMUser: ...

    @abstractmethod
    def find_by_email(self, email: str) -> IAMUser: ...
