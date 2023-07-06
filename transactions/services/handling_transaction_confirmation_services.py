from unittest.mock import MagicMock
from decimal import Decimal


def send_transaction_confirmation(sender_address: str, recipient_address: str, amount: Decimal) -> dict:
    api_mock: MagicMock = MagicMock()
    api_mock.abstract_method.return_value = {'status': True}
    response: dict = api_mock.abstract_method()

    return response
