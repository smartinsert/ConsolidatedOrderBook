from .action_handler import ActionHandler


class ModifyOrder(ActionHandler):

    def act_on(self, message, exchange_name):
        message_elements = message.split(':')[1].strip()
        order_elements = message_elements.split(',')
        order_id = order_elements[1].strip() + '_' + exchange_name
        quantity = int(order_elements[2].strip())
        self.order_book.modify(order_id, quantity)