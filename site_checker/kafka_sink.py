import msgpack
from kafka import KafkaProducer


class KafkaSink(object):
    """A data sink that posts data to a Kafka topic
    The sink is not thread safe and should not be shared across threads.

    Keyword Arguments:
        topic_name: topic to post data to.
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) Kafka cluster address this source connected to.
            Default port is 9092. If no servers are specified, 
            will default to localhost:9092.
        ssl_cafile: Filename of CA file to use in certificate verification.
        ssl_certfile: Filename of file in pem format containing
            the client certificate, as well as any ca certificates needed to
            establish the certificate's authenticity.
        ssl_keyfile: Filename containing the client private key. 
            Required for SSL based authentication.

        connection(obj): Transport channel override.

    """

    DEFAULT_TOPICNAME = "site_status"

    def __init__(self, topic_name:str=None,
                 bootstrap_servers='localhost',
                 ssl_cafile=None,
                 ssl_certfile=None,
                 ssl_keyfile=None,
                 connection=None):
        self.producer = connection or KafkaProducer(
            api_version=(1, 0, 0),
            security_protocol='SSL',
            bootstrap_servers=bootstrap_servers,
            ssl_cafile=ssl_cafile,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile,
            value_serializer=msgpack.packb)

        self.topic_name = topic_name or self.DEFAULT_TOPICNAME

    def post(self, msg) -> None:
        """Post a message to a configured topic
        
        Args:
            msg: A message to post 
        """

        self.producer.send(self.topic_name, msg)
        self.producer.flush()
