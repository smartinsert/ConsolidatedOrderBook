

class OrderBookLevel:
    def __init__(self, price: float, size: int):
        self.price = price
        self.size = size

    @property
    def get_price(self):
        return self.price

    @property
    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size
