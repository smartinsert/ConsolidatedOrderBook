import unittest
from utilities.action_handler import ConsolidatedOrderBook
from exceptions import OrderAlreadyExistsException, OrderDoesNotExistException
from utilities import OrderSide


class TestDuplicateOrderID(unittest.TestCase):
    def setUp(self) -> None:
        self.consolidated_order_book = ConsolidatedOrderBook()

    def test_duplicate_order_id_should_not_be_allowed(self):
        symbol = 'GOOG'
        order_id = '1'
        order_side = OrderSide.BUY
        quantity = 10
        price = 100.5
        self.consolidated_order_book.add(symbol, order_id, order_side, price, quantity)

        symbol = 'MSFT'
        order_id = '1'
        order_side = OrderSide.SELL
        quantity = 50
        price = 200.5

        with self.assertRaises(OrderAlreadyExistsException):
            self.consolidated_order_book.add(symbol, order_id, order_side, price, quantity)

        self.assertEquals(len(self.consolidated_order_book.bid_side_orders), 1)

    def test_non_existent_order_cannot_be_modified_or_cancelled(self):
        with self.assertRaises(OrderDoesNotExistException):
            self.consolidated_order_book.cancel(2)
        self.assertEqual(len(self.consolidated_order_book.bid_side_orders), 1)


if __name__ == '__main__':
    unittest.main()
