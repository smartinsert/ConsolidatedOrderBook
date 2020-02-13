import time
import threading
from utilities import ActionHandlerFactory
from facade import Exchange
from implementation import NYSE, NASDAQ

# amount of time when the data is no longer required. Possibly: EOD
END_OF_MARKET = 60


def read_messages(exchange: Exchange, show_message=None):
    start_time, current_time = time.time(), time.time()
    while True:
        try:
            message = exchange.request_message() if not show_message else show_message
            exchange_name = exchange.exchange_name if exchange else None
            print(f'{threading.current_thread().getName()}: {message}', sep='\n')
            handler = ActionHandlerFactory.get_action_for(message)
            handler.act_on(message, exchange_name)
            time.sleep(10)
            current_time = time.time()
        except StopIteration:
            print(f'End of messages from {exchange.exchange_name}', sep='\n')
            break
        if current_time - start_time > END_OF_MARKET:
            print(f'{threading.current_thread().getName()}: Market has closed !')
            break


if __name__ == '__main__':
    nyse_exchange_messages = threading.Thread(target=read_messages, name='NYSE EXCHANGE', args=[NYSE()])
    nasdaq_exchange_messages = threading.Thread(target=read_messages, name='NASDAQ EXCHANGE', args=[NASDAQ()])

    google_message_subscriber_1 = threading.Thread(target=read_messages,
                                                   name='TRADER 1',
                                                   args=[None, 'SHOW_LEVELS: GOOG'])
    google_message_subscriber_2 = threading.Thread(target=read_messages,
                                                   name='TRADER 2',
                                                   args=[None, 'SHOW_LEVELS: GOOG'])

    nyse_exchange_messages.start()
    nasdaq_exchange_messages.start()

    google_message_subscriber_1.start()
    google_message_subscriber_2.start()

    nyse_exchange_messages.join()
    nasdaq_exchange_messages.join()

    google_message_subscriber_1.join()
    google_message_subscriber_2.join()

