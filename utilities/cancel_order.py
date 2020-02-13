from .action_handler import ActionHandler


class CancelOrder(ActionHandler):

    def act_on(self, message, exchange_name):
        message_elements = message.split(':')[1].strip()
        order_elements = message_elements.split(',')
        self.order_book.cancel(order_elements[0].strip() + '_' + exchange_name)