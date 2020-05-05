from collections import namedtuple
from datetime import datetime
from time import sleep
from timeit import default_timer as timer
import re
import requests


def _request_matches(r, regexp) -> bool:
    """Check if request has data and that data matches give regular expresssion

    Args:
        r: HTTP call result from a status provider, must implement raise_for_status() and .text
        regexp: Compiler regular expression to search for in the HTTP request text field.

    Returns:
        True if a match is found, false if not and None if request contains no .text property
    """

    try:
        r.raise_for_status()
        text = r.text
        return regexp.search(text) is not None
    except:
        return None


def check_status(url: str, regexp, status_provider, src='localhost') -> dict:
    """Check status code of a given Url

    Args:
        url: URL-string of a resource to check with HTTP GET request.
        regexp: Regular expression to check respose against if any
        src: Identifier of a requestor used for reporting and returned as result.src
        status_provider: Callable used to get a status of a resource.

    Returns:
        Object representing a status of the given resource
    """
    ts = datetime.now()

    start_time = timer()
    r = status_provider(url)
    end_time = timer()

    return {
        'timestamp': str(ts),
        'src': src,
        'target': url,
        'time': (end_time - start_time),
        'code': r.status_code,
        'has_match': _request_matches(r, regexp) if regexp else None
    }


class RestStatusPoller:
    """A source of REST-resourse status checks.
    This Source is issuing REST Get requests to a give resource URL 
    and yelds a dict descriding resource status.

    The source is designed to be used as iterable:
    for data in source:
        process(data)

    Keyword Arguments:
        url: URL of the resource to check status
        interval: (int or None): time is sec to wait before the next check.
            If None is given, the check is performed only once.
        regexp (str or None): regular expression to search for in the response body, if any.
            If None is given - no search is performed and 'has_match' field of the status
            responce is set to None
        provider(callable on None): a resource status provider override.
            If None is give - requests.get is used. Default is None.
    """

    def __init__(self, url, interval, regexp, provider=None):
        self.url = url
        self.interval = interval
        self.pattern = re.compile(regexp) if regexp else None
        self.__value_provide = provider or (lambda x: requests.get(
            x, headers={'content-type': 'application/json'}))
        self.__iter_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iter_count > 0:
            if self.interval is not None:
                sleep(self.interval)
            else:
                raise StopIteration()
        self.__iter_count += 1

        return check_status(self.url, self.pattern, self.__value_provide)
