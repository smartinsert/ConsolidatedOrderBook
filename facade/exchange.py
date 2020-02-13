from abc import abstractmethod
from utilities import SingletonABCMeta


class Exchange(metaclass=SingletonABCMeta):
    def __init__(self, name):
        self.name = name
        self.messages = list()
        self.yield_messages = self._yield_messages()

    @property
    def exchange_name(self):
        return self.name

    @abstractmethod
    def set_messages(self):
        raise NotImplementedError

    def _yield_messages(self):
        for message in self.messages:
            yield message

    def request_message(self):
        return next(self.yield_messages)

