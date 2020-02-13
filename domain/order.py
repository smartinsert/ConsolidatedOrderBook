from utilities import OrderSide


class Order:
    def __init__(self, order_id: str, symbol: str, order_side: OrderSide, price: float, size: int):
        self.order_id = order_id
        self.symbol = symbol
        self.order_side = order_side
        self.price = price
        self.size = size

    @property
    def get_order_id(self) -> str:
        return self.order_id

    @property
    def get_symbol(self) -> str:
        return self.symbol

    @property
    def get_order_side(self) -> OrderSide:
        return self.order_side

    @property
    def get_price(self) -> float:
        return self.price

    @property
    def get_size(self) -> int:
        return self.size

    @property
    def is_buy(self) -> bool:
        return self.order_side == OrderSide.BUY

    @property
    def is_sell(self) -> bool:
        return self.order_side == OrderSide.SELL
