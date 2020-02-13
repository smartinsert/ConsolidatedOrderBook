from .action_handler import ActionHandler


class TopOfTheBook(ActionHandler):

    def act_on(self, message, exchange_name):
        message_elements = message.split(':')[1].strip()
        book_elements = message_elements.split(',')
        symbol = book_elements[0].strip()
        best_bid_price = float(book_elements[1].strip())
        best_bid_size = float(book_elements[2].strip())
        best_offer_price = float(book_elements[3].strip())
        best_offer_size = float(book_elements[4].strip())
        self.order_book.handle_top_of_the_book(symbol, best_bid_price, best_bid_size, best_offer_price, best_offer_size)