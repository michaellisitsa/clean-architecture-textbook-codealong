from decimal import Decimal
from typing import Union

from placing_bid.money import Money
from placing_bid.currency import Currency


def get_dollars(amount: Union[Decimal, str, float, int]) -> Money:
    return Money(Currency.USD, amount)
