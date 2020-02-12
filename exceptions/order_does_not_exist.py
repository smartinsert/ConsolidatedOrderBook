class OrderDoesNotExistException(Exception):
    def __init__(self, order_id):
        super().__init__(f'{order_id} does not exist')
