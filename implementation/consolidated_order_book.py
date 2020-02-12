from facade import OrderBook
from domain import Order, OrderBookLevel
from utilities import synchronized
from exceptions import OrderDoesNotExistException, OrderQuantityMismatchException, OrderAlreadyExistsException


class ConsolidatedOrderBook(OrderBook):
    def __init__(self):
        self.bid_side_orders = list()
        self.ask_side_orders = list()
        self.order_id_to_order_side = dict()
        self.bid_price_to_order_book_level = dict()
        self.ask_price_to_order_book_level = dict()

    @synchronized
    def add(self, order_id: int, side: str, price: float, size: int):
        if not self._does_order_exist(order_id):
            new_order = Order(order_id=order_id, order_side=side, price=price, size=size)
            self.order_id_to_order_side.setdefault(order_id, new_order)
            self._add_order(new_order)
        else:
            raise OrderAlreadyExistsException(order_id)

    @synchronized
    def modify(self, order_id: int, size: int):
        pass

    @synchronized
    def cancel(self, order_id: int):
        pass

    @synchronized
    def show_top_levels(self, number_of_levels=5):
        pass

    def _add_order(self, order: Order) -> None:
        if order.is_buy:
            self.bid_side_orders.append(order)
            ConsolidatedOrderBook._update_order_book_level(order, self.bid_price_to_order_book_level)
        elif order.is_sell:
            self.ask_side_orders.append(order)

    @staticmethod
    def _update_order_book_level(order: Order, price_to_order_book_level):
        if order.get_price not in price_to_order_book_level:
            order_book_level = OrderBookLevel(order.get_price, order.get_size)
            price_to_order_book_level.setdefault(order.get_price, order_book_level)
        else:
            existing_level = price_to_order_book_level.get(order.get_price)
            new_size = existing_level.get_size + order.get_size
            existing_level.set_size(new_size)

    def _does_order_exist(self, order_id: int) -> bool:
        return order_id in self.order_id_to_order_side.keys()