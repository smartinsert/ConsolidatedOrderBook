from typing import List
from facade import OrderBook
from domain import Order, OrderBookLevel
from utilities import synchronized, OrderSide
from exceptions import OrderDoesNotExistException, OrderQuantityMismatchException, OrderAlreadyExistsException


class ConsolidatedOrderBook(OrderBook):
    def __init__(self):
        self.bid_side_orders = list()
        self.offer_side_orders = list()
        self.order_id_to_order_side = dict()
        self.bid_side_to_order_book_level = dict()
        self.offer_side_to_order_book_level = dict()

    @synchronized
    def add(self, symbol: str, order_id: str, side: OrderSide, price: float, size: int):
        if not self._does_order_exist(order_id):
            new_order = Order(order_id=order_id, symbol=symbol, order_side=side, price=price, size=size)
            self.order_id_to_order_side.setdefault(order_id, new_order.get_order_side)
            self._add_order(new_order)
        else:
            raise OrderAlreadyExistsException(order_id)

    @synchronized
    def modify(self, order_id: str, size: int):
        order = self._cancel_order_with(order_id)
        modified_order = Order(order_id, order.get_symbol, order.get_order_side, order.get_price, size)
        self._add_order(modified_order)

    @synchronized
    def cancel(self, order_id: str) -> None:
        self._cancel_order_with(order_id)

    def _cancel_order_with(self, order_id: str) -> Order:
        if self._does_order_exist(order_id):
            order_side = self.order_id_to_order_side.get(order_id)
            if order_side == OrderSide.BUY:
                order = ConsolidatedOrderBook._cancel_order(order_id=order_id,
                                                            specified_side_orders=self.bid_side_orders)
                ConsolidatedOrderBook._remove_order_quantity_from_order_level(order, self.bid_side_to_order_book_level)
            else:
                order = ConsolidatedOrderBook._cancel_order(order_id=order_id,
                                                            specified_side_orders=self.offer_side_orders)
                ConsolidatedOrderBook._remove_order_quantity_from_order_level(order, self.bid_side_to_order_book_level)
            return order
        else:
            raise OrderDoesNotExistException(order_id)

    @synchronized
    def handle_top_of_the_book(self, symbol: str, best_bid_price: float, best_bid_size: int,
                               best_offer_price: float, best_offer_size: int):
        required_bid_keys = [bid for bid in self.bid_side_to_order_book_level if bid[0] == symbol]
        required_offer_keys = [offer for offer in self.offer_side_to_order_book_level if offer[0] == symbol]

        all_bids = set([key[0] for key in required_bid_keys])
        all_offers = set([key[0] for key in required_bid_keys])

        if best_bid_price in all_bids:
            for index, bid_key in required_bid_keys:
                if bid_key == (symbol, best_bid_price):
                    order_level = self.bid_side_to_order_book_level.get(bid_key)
                    order_level.set_size(best_bid_size)
                    break
        else:
            self.bid_side_to_order_book_level.setdefault((symbol, best_bid_price),
                                                         OrderBookLevel(best_bid_price, best_bid_size))

        if best_offer_price in all_offers:
            for index, offer_key in required_offer_keys:
                if offer_key == (symbol, best_offer_price):
                    order_level = self.offer_side_to_order_book_level.get(offer_key)
                    order_level.set_size(best_offer_size)
                    break
        else:
            self.offer_side_to_order_book_level.setdefault((symbol, best_bid_price),
                                                           OrderBookLevel(best_offer_price, best_offer_size))

    @synchronized
    def show_top_levels(self, symbol, number_of_levels=5) -> None:
        if not len(self.bid_side_to_order_book_level) and not len(self.offer_side_to_order_book_level):
            print('Prices unavailable')
        else:
            sorted_bids = sorted(self.bid_side_to_order_book_level, key=lambda x: x[1], reverse=True)
            sorted_offers = sorted(self.offer_side_to_order_book_level, key=lambda x: x[1])
            required_bid_keys = [bid for bid in sorted_bids if bid[0] == symbol]
            required_offer_keys = [offer for offer in sorted_offers if offer[0] == symbol]
            current_level = 0
            while current_level <= len(required_bid_keys) and current_level <= len(required_offer_keys):
                if current_level > number_of_levels:
                    break
                try:
                    required_bid_level = self.bid_side_to_order_book_level.get(required_bid_keys[current_level])
                    bid_price = required_bid_level.get_price
                    bid_size = required_bid_level.get_size
                except IndexError:
                    bid_price, bid_size = 0, 0
                try:
                    required_offer_level = self.offer_side_to_order_book_level.get(required_offer_keys[current_level])
                    offer_price = required_offer_level.get_price
                    offer_size = required_offer_level.get_size
                except IndexError:
                    offer_price, offer_size = 0, 0
                print(Response(level_number=current_level,
                               bid_price=bid_price, bid_size=bid_size,
                               offer_price=offer_price, offer_size=offer_size),
                      sep='\n')
                current_level += 1

    def _add_order(self, order: Order) -> None:
        if order.is_buy:
            self.bid_side_orders.append(order)
            ConsolidatedOrderBook._update_order_book_level(order, self.bid_side_to_order_book_level)
        elif order.is_sell:
            self.offer_side_orders.append(order)
            ConsolidatedOrderBook._update_order_book_level(order, self.offer_side_to_order_book_level)

    @staticmethod
    def _cancel_order(order_id: str, specified_side_orders: List[Order]) -> Order:
        required_order_index = None
        for index, order in enumerate(specified_side_orders):
            if order.get_order_id == order_id:
                required_order_index = index
                break
        if required_order_index is not None:
            return specified_side_orders.pop(required_order_index)
        else:
            raise OrderDoesNotExistException(order_id)

    @staticmethod
    def _update_order_book_level(order: Order, side_to_order_book_level):
        if (order.get_symbol, order.get_price) not in side_to_order_book_level:
            order_book_level = OrderBookLevel(order.get_price, order.get_size)
            side_to_order_book_level.setdefault((order.get_symbol, order.get_price), order_book_level)
        else:
            existing_level = side_to_order_book_level.get((order.get_symbol, order.get_price))
            new_size = existing_level.get_size + order.get_size
            existing_level.set_size(new_size)

    @staticmethod
    def _remove_order_quantity_from_order_level(found_order: Order, side_to_order_book_level):
        existing_order_book_level = side_to_order_book_level.get((found_order.get_symbol, found_order.get_price))
        remaining_size = existing_order_book_level.get_size - found_order.get_size
        if remaining_size < 0:
            raise OrderQuantityMismatchException(f'Could not modify the order book level as existing order level '
                                                 f'quantity is {existing_order_book_level.get_size} and '
                                                 f'quantity to remove is {found_order.get_size}')
        elif remaining_size == 0:
            del side_to_order_book_level[(found_order.get_symbol, found_order.get_price)]
        else:
            existing_order_book_level.set_size(remaining_size)

    def _does_order_exist(self, order_id: str) -> bool:
        return order_id in self.order_id_to_order_side.keys()


class Response:
    def __init__(self, level_number, bid_price, bid_size, offer_price, offer_size):
        self.level_number = level_number
        self.bid_price = bid_price
        self.bid_size = bid_size
        self.offer_price = offer_price
        self.offer_size = offer_size

    def __repr__(self):
        return f'Level {self.level_number}: {self.bid_size}, {self.bid_price}, {self.offer_price}, {self.offer_size}'