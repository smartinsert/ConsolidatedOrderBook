from utilities import OrderSide


class Order:
    def __init__(self, order_id: int, order_side: str, price: float, size: int):
        self.order_id = order_id
        self.order_side = OrderSide(order_side)
        self.price = price
        self.size = size

    @property
    def get_order_id(self) -> int:
        return self.order_id

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
