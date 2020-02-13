from utilities import ActionHandler
from exceptions import UnknownMessageException
from .add_order import AddOrder
from .modify_order import ModifyOrder
from .cancel_order import CancelOrder
from .top_of_the_book import TopOfTheBook
from .show_levels import ShowLevels


class ActionHandlerFactory:
    @staticmethod
    def get_action_for(line: str) -> ActionHandler:
        if ActionHandlerFactory._is_add_order(line):
            return AddOrder()
        elif ActionHandlerFactory._is_modify_order(line):
            return ModifyOrder()
        elif ActionHandlerFactory._is_cancel_order(line):
            return CancelOrder()
        elif ActionHandlerFactory._is_top_of_the_book_message(line):
            return TopOfTheBook()
        elif ActionHandlerFactory._is_show_level_message(line):
            return ShowLevels()
        else:
            raise UnknownMessageException(f'Unknown message encountered in {line}')

    @staticmethod
    def _is_add_order(line: str) -> bool:
        return line.split(':')[0] == 'NEW_ORDER'

    @staticmethod
    def _is_modify_order(line: str) -> bool:
        return line.split(':')[0] == 'MODIFY_ORDER'

    @staticmethod
    def _is_cancel_order(line: str) -> bool:
        return line.split(':')[0] == 'CANCEL_ORDER'

    @staticmethod
    def _is_top_of_the_book_message(line: str) -> bool:
        return line.split(':')[0] == 'TOP_OF_THE_BOOK'

    @staticmethod
    def _is_show_level_message(line: str) -> bool:
        return line.split(':')[0] == 'SHOW_LEVELS'
