from .action_handler import ActionHandler


class ShowLevels(ActionHandler):

    def act_on(self, message, exchange_name):
        symbol = message.split(':')[1].strip()
        self.order_book.show_top_levels(symbol=symbol)