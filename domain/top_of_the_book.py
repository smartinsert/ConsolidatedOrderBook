

class TopOfTheBook:
    def __init__(self, symbol:str, best_bid_price: float, best_bid_size: int,
                 best_ask_price: float, best_ask_size: int):
        self._symbol = symbol
        self._best_bid_price = best_bid_price
        self._best_bid_size = best_bid_size
        self._best_ask_price = best_ask_price
        self._best_ask_size = best_ask_size

    def __str__(self):
        return f'Symbol: {self._symbol}: Best Bid Price: {self._best_bid_price} Best Bid Size: {self._best_bid_size} ' \
               f'Best Ask Price: {self._best_ask_price} Best Ask Size: {self._best_ask_size}'

    @property
    def get_symbol(self):
        return self._symbol

    @property
    def get_best_bid_price(self):
        return self._best_bid_price

    @property
    def get_best_bid_size(self):
        return self._best_bid_size

    @property
    def get_best_ask_price(self):
        return self._best_ask_price

    @property
    def get_best_ask_size(self):
        return self._best_ask_size