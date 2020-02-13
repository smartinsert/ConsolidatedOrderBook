from implementation import ConsolidatedOrderBook


class ActionHandler:
    def __init__(self):
        self.order_book = ConsolidatedOrderBook()

    def act_on(self, message, exchange_name):
        raise NotImplementedError
