from utilities import SingletonABCMeta
from abc import abstractmethod


class OrderBook(metaclass=SingletonABCMeta):
    @abstractmethod
    def add(self, symbol: str, order_id: str, side: str, price: float, size: int):
        raise NotImplementedError

    @abstractmethod
    def modify(self, order_id: str, size: int):
        raise NotImplementedError

    @abstractmethod
    def cancel(self, order_id: str):
        raise NotImplementedError

    @abstractmethod
    def show_top_levels(self, number_of_levels):
        raise NotImplementedError

