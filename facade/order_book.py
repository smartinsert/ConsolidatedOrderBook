from abc import ABC, abstractmethod


class OrderBook(ABC):
    @abstractmethod
    def add(self, order_id: int, side: str, price: float, size: int):
        raise NotImplementedError

    @abstractmethod
    def modify(self, order_id: int, size: int):
        raise NotImplementedError

    @abstractmethod
    def cancel(self, order_id: int):
        raise NotImplementedError

    @abstractmethod
    def show_top_levels(self, number_of_levels):
        raise NotImplementedError

