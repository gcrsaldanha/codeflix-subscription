class DomainException(Exception):
    """Base domain exception"""


class SubscriptionConflictError(DomainException):
    """Raised when subscription rules are violated"""


class RenewSubscriptionError(Exception):
    """Raised when renew rules are violated"""


class UpgradeSubscriptionError(Exception):
    """Raised when activation rules are violated"""


class UserAlreadyExistsError(Exception):
    """Raised when trying to create a user that already exists"""
