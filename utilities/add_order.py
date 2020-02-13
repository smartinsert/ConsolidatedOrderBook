from .action_handler import ActionHandler
from .order_side import OrderSide


class AddOrder(ActionHandler):

    def act_on(self, message, exchange_name):
        message_elements = message.split(':')[1].strip()
        order_elements = message_elements.split(',')
        symbol = order_elements[0].strip()
        price = float(order_elements[1].strip())
        side = OrderSide(order_elements[2].strip())
        quantity = int(order_elements[3].strip())
        order_id = order_elements[4].strip() + '_' + exchange_name
        self.order_book.add(symbol, order_id, side, price, quantity)
