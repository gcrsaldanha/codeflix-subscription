from src.domain.plan import Plan
from src.domain.user_account import UserAccount


class InMemoryUserAccountRepository:
    def __init__(self, user_accounts: list[UserAccount] = None) -> None:
        self.user_accounts = user_accounts or []

    def save(self, user_account: UserAccount) -> None:
        self.user_accounts.append(user_account)
