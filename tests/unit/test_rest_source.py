import unittest

from site_checker import RestStatusPoller


class _MockStatus():
    def __init__(self, code, text, is_error):
        self.status_code = code
        self.text = text
        self._is_error = is_error

    def raise_for_status(self):
        if self._is_error:
            raise Exception('error status')


class _MockStatusProvider:
    def __init__(self, code, text=None, is_error=False):
        self.status_code = code
        self.text = text
        self._is_error = is_error

    def __call__(self, url):
        return _MockStatus(self.status_code, self.text, self._is_error)


class TestRestStatusPoller(unittest.TestCase):
    def test_poll_once_no_regexp(self):
        """
        Test status poller once with no regexp to search the reposnse body for.
        """
        mock_target = "what://ever"
        mock_provider = _MockStatusProvider(code=201, text="ok")
        poller = RestStatusPoller(
            url=mock_target, regexp=None, interval=None, provider=mock_provider)

        counter = 0
        for event in poller:
            counter += 1

            self.assertEqual(event['code'], 201)
            self.assertEqual(event['target'], mock_target)
            self.assertEqual(event['has_match'], None)

        self.assertEqual(counter, 1)

    def test_poll_once_with_regexp(self):
        """
        Test status poller once with regexp to search the reposnse body for.
        """
        mock_target = "what://ever"
        mock_provider = _MockStatusProvider(code=201, text="ok")
        poller = RestStatusPoller(
            url=mock_target, regexp='ok', interval=None, provider=mock_provider)

        counter = 0
        for event in poller:
            counter += 1

            self.assertEqual(event['code'], 201)
            self.assertEqual(event['target'], mock_target)
            self.assertEqual(event['has_match'], True)

        self.assertEqual(counter, 1)


if __name__ == '__main__':
    unittest.main()
