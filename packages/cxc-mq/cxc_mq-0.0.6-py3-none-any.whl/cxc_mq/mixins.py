class InitiateConfigMixin():
    def init_config(self, config):
        self.HOST = config.get("host", "localhost")
        self.PORT = config.getint("port", 5672)

        self.USERNAME = config.get("username")
        self.PASSWORD = config.get("password")

        self.VIRTUAL_HOST = config.get("vhost")

        self.EXCHANGE_NAME = config.get("exchange_name")
        self.EXCHANGE_TYPE = config.get("exchange_type")

        self.QUEUE_NAME = config.get("queue_name")
        self.ROUTING_KEY = config.get("routing_key")
