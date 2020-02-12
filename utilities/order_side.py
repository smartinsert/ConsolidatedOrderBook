from enum import Enum


class OrderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

    def __str__(self):
        return self.value