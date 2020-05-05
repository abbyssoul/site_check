import unittest

from check_persister import DbSink


class _FakeConnection:
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def cursor(self):
        return self

    def execute(self, query, params):
        self.last_query = query
        self.last_param = params


class TestDbSink(unittest.TestCase):
    def test_post(self):
        """
        Test that DbSink post executes query with passed in message
        """
        mock_connection = _FakeConnection()
        sink = DbSink(None, connection=mock_connection)
        sink.post("hello world")

        self.assertEqual(mock_connection.last_param, "hello world")
        self.assertEqual(mock_connection.last_query,
                         sink.insert_query.format(sink.DEFAULT_TABLENAME))


if __name__ == '__main__':
    unittest.main()
