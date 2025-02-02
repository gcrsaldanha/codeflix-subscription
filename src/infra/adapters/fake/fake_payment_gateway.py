from src.application.ports import PaymentGateway
from src.domain.value_objects import PaymentResult, MonetaryValue


class FakePaymentGateway(PaymentGateway):
    def __init__(self, fake_result: PaymentResult) -> None:
        self.fake_result = fake_result

    def charge(self, amount: MonetaryValue, token: str) -> PaymentResult:
        return self.fake_result
