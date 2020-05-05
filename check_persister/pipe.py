import logging

from .db_sink import DbSink
from .kafka_source import KafkaSource

log = logging.getLogger(__name__)


class Pipe:
    """Convenience class for teing together data source and sink.
     Source is expected to be an iterable producing data.
     Sink is a consumer of data produced by source.

     Note: 
        it is possible to use an iterable such as list as data source.

    """

    def __init__(self, source_config, sink_config, source=None, sink=None, mapper=lambda x: x.value):
        self.mapper = mapper
        self.sink = sink or DbSink(**sink_config)
        self.source = source if source is not None else KafkaSource(
            **source_config)

    def loop(self) -> None:
        "Iterate over data in the source and feed that data to the sink"

        for status in self.source:
            log.info(f'Status update: {status}')
            try:
                self.sink.post(self.mapper(status))
            except:
                log.error(f'Failed to post a message... skipping')

