import unittest

from check_persister import Pipe


class _MockSink:
    def __init__(self):
        self.messages_proccessed = 0

    def post(self, message):
        self.messages_proccessed += 1
        self.last_message = message


class TestRecorder(unittest.TestCase):
    def test_recording(self):
        """
        Test that Recorder passes events from source to sink
        """
        mock_sink = _MockSink()
        source = ["msg1", "msg2", "msg3"]

        recorder = Pipe(None, None, source=source, sink=mock_sink, mapper=lambda x: x)
        recorder.loop()

        self.assertEqual(mock_sink.messages_proccessed, 3)
        self.assertEqual(mock_sink.last_message, "msg3")


if __name__ == '__main__':
    unittest.main()
