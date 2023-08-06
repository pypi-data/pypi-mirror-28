import pika
import logging
import threading

from cxc_toolkit.patterns.singleton import SingletonMixin

from cxc_mq.mixins import InitiateConfigMixin

logger = logging.getLogger(__name__)


class Publisher(SingletonMixin, InitiateConfigMixin):
    def __init__(self, config=None, event=None):
        self.init_config(config)

        self.PUBLISH_INTERVAL = config.get("publish_interval", 1)

        credentials = pika.PlainCredentials(username=self.USERNAME,
                                            password=self.PASSWORD)
        conn_params = pika.ConnectionParameters(host=self.HOST,
                                                port=self.PORT,
                                                virtual_host=self.VIRTUAL_HOST,
                                                credentials=credentials,
                                                connection_attempts=3,
                                                heartbeat=3600)

        self._event = event

        self._connection = None
        self._channel = None
        self._deliveries = []
        self._acked = 0
        self._nacked = 0
        self._message_number = 0
        self._stopping = False
        self._conn_params = conn_params
        self._closing = False

    def connect(self):
        logger.info('Connecting to %s', self._conn_params.host)
        if self._connection:
            self._connection.connect()
        else:
            self._connection = pika.SelectConnection(
                parameters=self._conn_params,
                on_open_callback=self.on_connection_open,
                on_close_callback=self.on_connection_closed,
                stop_ioloop_on_close=False)
        return self._connection

    def on_connection_open(self, unused_connection):
        logger.info('Connection opened')
        self.open_channel()

    def on_connection_closed(self, connection, reply_code, reply_text):
        logger.warning('Connection closed, reopening in 1 seconds: (%s) %s',
                       reply_code, reply_text)
        self._connection.add_timeout(1, self.reconnect)

    def reconnect(self):
        self.connect()

    def open_channel(self):
        logger.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        logger.info('Channel opened')
        self._channel = channel
        self.setup_exchange(self.EXCHANGE_NAME)

    def setup_exchange(self, exchange_name):
        logger.info('Declaring exchange%s', exchange_name)
        self._channel.exchange_declare(exchange=exchange_name,
                                       exchange_type=self.EXCHANGE_TYPE,
                                       passive=False,
                                       durable=False,
                                       auto_delete=False)

        self._event.set()

    def publish_message(self, message=""):
        msg_props = pika.BasicProperties()
        msg_props.content_type = "text/plain"

        self._channel.basic_publish(body=message,
                                    exchange=self.EXCHANGE_NAME,
                                    properties=msg_props,
                                    routing_key=self.ROUTING_KEY)

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()


default_event = threading.Event()


def async_build_connection(event=default_event):
    t = threading.Thread(target=build_connection, args=(event,))
    t.daemon = True
    t.start()


def build_connection(event):
    publisher = Publisher.instance(event=event)
    publisher.run()


def async_publish_message(message, event=default_event):
    t = threading.Thread(target=publish, args=(message, event))
    t.daemon = True
    t.start()


def publish(message, event):
    publisher = Publisher.instance()
    event.wait()
    publisher.publish_message(message)


def main():
    async_build_connection()
    async_publish_message("Hi! I'm a message for test.")
    async_publish_message("Hi! I'm another message for test.")
