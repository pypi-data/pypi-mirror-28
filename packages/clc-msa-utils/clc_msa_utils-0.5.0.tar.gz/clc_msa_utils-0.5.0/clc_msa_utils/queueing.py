import json
import logging
import pika


class QueueConsumer:
    _config = {}
    _logger = logging.getLogger('QueueConsumer')

    def __init__(self, config={}):
        _config = config
        self._setup_logging()

    def _setup_logging(self):
        numeric_level = logging.INFO
        if self._config.get('logging_level'):
            numeric_level = getattr(logging, self._config.get('logging_level'), logging.INFO)
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        self._logger.setLevel(numeric_level)

    def _configure_listener(self, callback):
        credentials = pika.PlainCredentials(self._config['auth']['user'], self._config['auth']['password'])
        parameters = pika.ConnectionParameters(self._config['host'], self._config['port'], '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=self._config['queue'], durable=True)
        channel.queue_bind(queue=self._config['queue'], exchange=self._config['exchange']['name'],
                           routing_key=self._config['binding_key'])

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue=self._config['queue'])

        channel.start_consuming()

    def get_config(self):
        return self._config

    def listen(self, callback):
        self._configure_listener(callback)


class QueueProducer:
    _config = {}
    _logger = logging.getLogger('QueueProducer')
    _queue_channel = None

    def __init__(self, config={}):
        _config = self._normalize_config(config)
        self._setup_logging()
        self._configure_producer()

    def _setup_logging(self):
        numeric_level = logging.INFO
        if self._config.get('logging_level'):
            numeric_level = getattr(logging, self._config.get('logging_level'), logging.INFO)
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        self._logger.setLevel(numeric_level)

    def _configure_producer(self):
        self._logger.debug("Configuring queue producer with config:\n%s" % self._config)
        credentials = pika.PlainCredentials(self._config['auth']['user'], self._config['auth']['password'])
        parameters = pika.ConnectionParameters(self._config['host'], self._config['port'], '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        if 'create' in self.config['exchange'] and self._config['exchange']['create']:
            self._logger.debug("Exchange is being ensured present based on configuration...")
            channel.exchange_declare(exchange=self._config['exchange']['name'],
                                     exchange_type=(self._config['exchange']['type'] if 'type' in self._config['exchange'] else 'direct'),
                                     arguments=(self._config['exchange']['arguments'] if 'arguments' in self._config['exchange'] else {}),
                                     durable=(self._config['exchange']['durable'] if 'durable' in self._config['exchange'] else True))

        self._queue_channel = channel

    def _normalize_config(self, config):
        return config

    def publish(self, message=None):
        self._logger.info("Publishing message to exchange '%s' with binding key '%s'" % (self.config['exchange']['name'], self._config['binding_key']))
        self._logger.debug("Message:\n%s" % json.dumps(message, indent=4))
        self._queue_channel.basic_publish(exchange=self._config['exchange']['name'],
                                          routing_key=(self._config['binding_key'] if 'binding_key' in self._config else '#'),
                                          body=json.dumps(message),
                                          properties=pika.BasicProperties(delivery_mode=2,  # make message persistent
                                                                          content_type='application/json'))

    def get_config(self):
        return self._config



class QueueFactory():
    """
    QueueFactory provides helper methods for simply passing in a configuration
    and having producers/consumers created based on that config.  Additionally,
    there will be builder style methods available for setting/overriding configuration
    prior to generating producers/consumers.

    Currently, this solution is satisfying making a connection using AMQP which is compatible with
    RabbitMQ and ActiveMQ.  It could be enhanced to provide further abstraction and provide
    connections to other Queue services in theory.
    """

    _config = {}
    _logger = logging.getLogger('QueueFactory')
    _consumers = {}
    _producers = {}

    def __init__(self):
        self._setup_logging()
        self._logger.info("Initializing QueueFactory...")


    def _setup_logging(self):
        numeric_level = logging.INFO
        if self._config.get('logging_level'):
            numeric_level = getattr(logging, self._config.get('logging_level'), logging.INFO)
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        self._logger.setLevel(numeric_level)


    def create_consumers(self, queue_config):
        """
        Example Consumer Queue Configuration:
        {
          "queue_config": [
            {
              "name": "name-to-reference-this-connection",
              "type": "consumer",
              "exchange": {
                "name": "name-of-exchange",
                "type": "direct | fanout | etc",
                "arguments": {"x-delayed-type": "topic"},
                "durable": true | false
              },
              "queue": "name-of-queue",
              "binding_key": "#",
              "host": "rabbitmq-host",
              "port": "5672",
              "auth": {
                "user": "guest",
                "password": "guest"
              }
            }
          ]
        }
        """

        self._logger.debug("Setting up consumers for the following configuration:\n%s" % queue_config)
        if 'queue_config' in queue_config:
            queue_config = queue_config['queue_config']

        for config in queue_config:
            if 'type' in config['exchange'] and 'consumer' == config['exchange']['type']:
                consumer = QueueConsumer(config)
                self._consumers[config['name']] = consumer

        return self._consumers

    def create_producers(self, queue_config):
        """
        Example Producer Queue Configuration:
        {
            "queue_config": [
                {
                    "name": "name-to-reference-this-connection",
                    "type": "producer",
                    "exchange": {
                        "name": "name-of-exchange",
                        "create": true | false (whether or not to ensure exchange is present),
                        "type": "direct | fanout | etc",
                        "arguments": {"x-delayed-type": "topic"},
                        "durable": true | false
                    },
                    "binding_key": "#",
                    "host": "rabbitmq-host",
                    "port": "5672",
                    "auth": {
                        "user": "guest",
                        "password": "guest"
                    }
                }
            ]
        }
        """

        self._logger.debug("Setting up producers for the following configuration:\n%s" % queue_config)
        if 'queue_config' in queue_config:
            queue_config = queue_config['queue_config']

        for config in queue_config:
            if 'type' in config['exchange'] and 'producer' == config['exchange']['type']:
                producer = QueueProducer(config)
                self._producers[config['name']] = producer

        return self._producers
