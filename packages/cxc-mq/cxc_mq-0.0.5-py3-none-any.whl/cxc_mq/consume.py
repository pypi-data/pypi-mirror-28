import pika
import logging
import threading

from cxc_mq.mixins import InitiateConfigMixin

logger = logging.getLogger(__name__)


class Consumer(InitiateConfigMixin):
    def __init__(self, config=None, process_func=None):
        """
        Initiate consumer, establish connection

        :param config: config dict for establish connection and receive data
        :param process_func: callback function for process income message
        :type config: dict
        :type process_func: function
        """
        # Initiate mq config with config first
        self.init_config(config)

        credentials = pika.PlainCredentials(username=self.USERNAME,
                                            password=self.PASSWORD)
        conn_params = pika.ConnectionParameters(host=self.HOST,
                                                port=self.PORT,
                                                virtual_host=self.VIRTUAL_HOST,
                                                credentials=credentials,
                                                connection_attempts=3,
                                                heartbeat=3600)

        self._process_func = process_func
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._conn_params = conn_params

    def connect(self):
        logger.info("Connecting to {}".format(self._conn_params.host))
        if self._connection:
            self._connection.connect()
        else:
            self._connection = pika.SelectConnection(
                parameters=self._conn_params,
                on_open_callback=self.on_connection_open,
                on_close_callback=self.on_connection_closed,
                stop_ioloop_on_close=False
            )
        return self._connection

    def on_connection_open(self, unused_connection):
        logger.info("Connection opened")
        self.open_channel()

    def on_connection_closed(self, connection, reply_code, reply_text):
        logger.warning("Connection closed, reopening in 1 seconds: (%s) %s",
                       reply_code, reply_text)
        self._connection.add_timeout(1, self.reconnect)

    def open_channel(self):
        logger.info("Creating a new channel")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        logger.info("Channel opened")
        self._channel = channel
        self.setup_exchange(self.EXCHANGE_NAME)

    def setup_exchange(self, exchange_name):
        logger.info("Declaring exchange%s", exchange_name)
        self._channel.exchange_declare(callback=self.on_exchange_declareok,
                                       exchange=exchange_name,
                                       exchange_type=self.EXCHANGE_TYPE,
                                       passive=False,
                                       durable=False,
                                       auto_delete=False)

    def on_exchange_declareok(self, unused_frame):
        logger.info("Exchange declared")
        self.setup_queue(self.QUEUE_NAME)

    def setup_queue(self, queue_name):
        logger.info("Declaring queue %s", queue_name)
        self._channel.queue_declare(callback=self.on_queue_declareok,
                                    queue=queue_name)

    def on_queue_declareok(self, method_frame):
        logger.info("Binding {} to {} with {}".format(self.EXCHANGE_NAME,
                                                      self.QUEUE_NAME,
                                                      self.ROUTING_KEY))
        self._channel.queue_bind(callback=self.on_bindok,
                                 queue=self.QUEUE_NAME,
                                 exchange=self.EXCHANGE_NAME,
                                 routing_key=self.ROUTING_KEY)

    def on_bindok(self, unused_frame):
        logger.info("Queue bound")
        self.start_consuming()

    def start_consuming(self):
        logger.info("Issuing consumer related RPC commands")
        self._consumer_tag = self._channel.basic_consume(
            consumer_callback=self.on_message,
            queue=self.QUEUE_NAME
        )

    def on_message(self, unused_channel, basic_deliver, properties, body):
        logger.info("Received message # {} from {}: {}".format(
            basic_deliver.delivery_tag, properties.app_id, body))
        logger.debug(self._process_func)
        if self._process_func:
            self._process_func(body)
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        logger.info("Acknowlegding message {}".format(delivery_tag))
        self._channel.basic_ack(delivery_tag)

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()


def async_start_consume(config=None, f=None):
    t = threading.Thread(target=start_consume, args=(config, f, ))
    t.daemon = True
    t.start()


def start_consume(config, f):
    consumer = Consumer(config, process_func=f)
    consumer.run()
