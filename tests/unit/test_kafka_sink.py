import unittest

from site_checker import KafkaSink


class _FakeConnection:
    def flush(self):
        return self

    def send(self, topic, message):
        self.last_topic = topic
        self.last_message = message


class TestKafkaSink(unittest.TestCase):
    def test_post(self):
        """
        Test that DbSink post executes query with passed in message
        """
        mock_connection = _FakeConnection()
        sink = KafkaSink(connection=mock_connection)
        sink.post("hello world")

        self.assertEqual(mock_connection.last_topic, sink.DEFAULT_TOPICNAME)
        self.assertEqual(mock_connection.last_message, "hello world")


if __name__ == '__main__':
    unittest.main()
