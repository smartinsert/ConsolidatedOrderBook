from facade import Exchange


class NASDAQ(Exchange):
    def __init__(self):
        super(NASDAQ, self).__init__('NASDAQ')
        self.set_messages()

    def set_messages(self):
        self.messages = ['NEW_ORDER: MSFT, 100, BUY, 10, 1',
                         'NEW_ORDER: GOOG, 101, SELL, 5, 2',
                         'NEW_ORDER: GOOG, 102, BUY, 20, 3'
                         'TOP_OF_THE_BOOK: TESLA, 50, 150, 51, 200',
                         'MODIFY_ORDER: MSFT, 1, 50']
