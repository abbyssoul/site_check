import msgpack
from kafka import KafkaConsumer


class KafkaSource:
    """A Kafka source of REST-resourse status checks

    The source is not thread safe and should not be shared across threads.
    The source is designed to be used as iterable:
    for data in source:
        process(data)

    Keyword Arguments:
        topic_name: topics to subscribe to.
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) Kafka cluster address this source connected to.
            Default port is 9092. If no servers are specified, 
            will default to localhost:9092.
        group_id (str or None): The name of the consumer group to join for dynamic
            partition assignment (if enabled), and to use for fetching and
            committing offsets. If None, auto-partition assignment (via
            group coordinator) and offset commits are disabled.
            Default: None
        ssl_cafile: Filename of CA file to use in certificate verification.
        ssl_certfile: Filename of file in pem format containing
            the client certificate, as well as any ca certificates needed to
            establish the certificate's authenticity.
        ssl_keyfile: Filename containing the client private key. 
            Required for SSL based authentication.

        connection(obj): Transport channel override.
    """

    DEFAULT_TOPICNAME = "site_status"
    DEFAULT_CONSUMERGROUP = "status_consumer_group"

    def __init__(self, topic_name: str,
                 bootstrap_servers=None,
                 group_id: str = None,
                 ssl_cafile: str = None,
                 ssl_certfile: str = None,
                 ssl_keyfile: str = None,
                 connection=None):
        self.consumer = KafkaConsumer(topic_name or self.DEFAULT_TOPICNAME,
                                      security_protocol='SSL',
                                      api_version=(1, 0, 0),
                                      group_id=group_id or self.DEFAULT_CONSUMERGROUP,
                                      bootstrap_servers=bootstrap_servers,
                                      ssl_cafile=ssl_cafile,
                                      ssl_certfile=ssl_certfile,
                                      ssl_keyfile=ssl_keyfile,
                                      value_deserializer=msgpack.unpackb)

    def __iter__(self):
        return iter(self.consumer)

    # def __next__(self):
    #     next_value = next(self.consumer)
    #     return next_value.value
