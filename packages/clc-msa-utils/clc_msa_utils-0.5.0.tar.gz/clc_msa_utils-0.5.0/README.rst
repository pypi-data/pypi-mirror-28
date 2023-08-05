=================================================
CenturyLink Cloud ManagedOS Python Utilities [1]_
=================================================

***************
Getting Started
***************

To install the ``clc_msa_utils`` package, use the command below.::

    pip3 install clc_msa_utils

*******
KVStore
*******

This is a utlitiy class that abstracts loading a configuration from Consul or ETCD. This class supports perodically
reloading the configuration from the configured key-value store, and notifing a callback method after reloading.
The following may be passed into the constructor, or pulled from env variables:

+------------------+-----------------------+--------------------------------------------+-----------+
| Constructor Arg  | Environment Variable  | Description                                | Default   |
+==================+=======================+============================================+===========+
| consul_host      | CONSUL_HOST           | Host for Consul                            | None      |
+------------------+-----------------------+--------------------------------------------+-----------+
| consul_port      | CONSUL_PORT           | Port for Consul                            | 8500      |
+------------------+-----------------------+--------------------------------------------+-----------+
| etcd_host        | ETCD_HOST             | Host for etcd                              | localhost |
+------------------+-----------------------+--------------------------------------------+-----------+
| etcd_port        | ETCD_PORT             | Port for etcd                              | 2379      |
+------------------+-----------------------+--------------------------------------------+-----------+
| kv_prefix        | KV_PREFIX             | Prefix for config path                     | ""        |
+------------------+-----------------------+--------------------------------------------+-----------+
| reload_seconds   | RELOAD_CONFIG_PERIOD  | Seconds between config reloads             | 20        |
+------------------+-----------------------+--------------------------------------------+-----------+
| reload_enabled   | RELOAD_ENABLED        | If true, reloads the config periodically.  | False     |
+------------------+-----------------------+--------------------------------------------+-----------+

TODO: Future Features
~~~~~~~~~~~~~~~~~~~~~~
* Logging Configuration: Will enable configuring logging by updating the specified configuration mechanism.
* Nested Configurations: Will enable you specify a list of prefixes to use to overlay configuration values.

Example Usage
~~~~~~~~~~~~~

.. code:: python
   :number-lines: 1

      from clc_msa_utils.kv_store import KVStore

        # Create config store
        kv_store = KVStore(
            kv_prefix=os.getenv('CONSUL_PREFIX') or os.getenv('ETCD_PREFIX', '/config/retry-listener'),
            reload_enabled=True
        )

        # Setup on_reload handler
        def initialize():
            kv_store.on_reload(dynamic_configuration)

        # Implement reload handler to check if attributes changed, and then perform some logic.
        def dynamic_configuration(old, new):
            if not old or old.get('exchange_configs') != new.get('exchange_configs') \
                or kv_store.attribute_changed("rabbit_host","rabbit_port","rabbit_user","rabbit_password","rabbit_queue_name"):
            setup_queue()

    # Use kv_store to pull configuration values.
    def setup_queue():
        rabbit_host = kv_store.get('rabbit_host', 'localhost')
        rabbit_port = int(kv_store.get('rabbit_port', 5672))


************
QueueFactory
************

This is a utility class that abstracts the creation of Queue Producers and Queue Consumers/Listeners.
The producers and consumers are constructed based on a configuration passed into their respective methods
as a parameter.  The following is an example JSON configuration of a Queue Consumer configuration that
could be stored in a key-value store such as ETCD or Consul. Notice that the `queue_config` attribute is
an array and can be all of the necessary configuration for both your Consumer and Producers.

.. code:: json

    {
      "queue_config": [
        {
          "name": "make_managed_request",
          "type": "consumer",
          "exchange": {
            "name": "managed_server",
            "type": "x-delayed-message",
            "arguments": {"x-delayed-type": "topic"},
            "durable": true
          },
          "queue": "make_managed_mos_cmdb",
          "binding_key": "requested.make_managed",
          "host": "rabbitmq.managed-services-dev.skydns.local",
          "port": "5672",
          "auth": {
            "user": "guest",
            "password": "guest"
          }
        }
      ]
    }

Example Usage
~~~~~~~~~~~~~

.. code:: python
   :number-lines: 1

        from clc_msa_utils.queueing import QueueFactory

        # Get config (eg. from kv_store)
        queue_config = kv_store.get('queue-config')

        # Initialize QueueFactory
        q_factory = QueueFactory()

        # Generate Queue Consumers (QueueConsumer)
        consumers = q_factory.create_consumers(queue_config)

        # Generate Queue Producers (QueueProducer)
        producers = q_factory.create_producers(queue_config)

        # Retrieve and use consumer based on name configured
        consumers['make_managed_request'].listen(callback_function)

        # Retrieve and use producer based on name configured
        producers['error'].publish({"error_details": "message about how you messed things up..."})



        def callback_function(ch, method, properties, body):
        ...

----

.. [1] This document is formatted using `reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_,
   with `reStructuredText directives <http://docutils.sourceforge.net/docs/ref/rst/directives.html>`_.
