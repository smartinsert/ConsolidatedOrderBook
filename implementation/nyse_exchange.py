from facade import Exchange


class NYSE(Exchange):
    def __init__(self):
        super(NYSE, self).__init__('NYSE')
        self.set_messages()

    def set_messages(self):
        self.messages = ['NEW_ORDER: GOOG, 100, BUY, 10, 1',
                         'TOP_OF_THE_BOOK: AMZN, 50, 150, 51, 200',
                         'MODIFY_ORDER: GOOG, 1, 50']
