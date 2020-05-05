#!/usr/bin/env python3
"""
 CLI driver used for controlling web-site status checker
"""

import fire
import logging

from site_checker import Pipe
import kafka_config
import rest_config


def _as_dict(module):
  return {setting: getattr(module, setting) for setting in dir(module) if not setting.startswith('_')}


def check_site(url: str = None, regexp: str = None, interval: int = None):
  """Main driver function - take command line params and run the rest resource check

  Args:
      url: override Resource URL to query. If None is given a value from rest_config is used.
      regexp: override regular expression to search for in the response text. If None is given a value from rest_config is used.
      interval: override query interval in sec. 0 means - query once. If None is given a value from rest_config is used.
  """
  logging.basicConfig(level=logging.INFO)

  # url, regexp, interval
  if url is not None:
    rest_config.url = url
  if regexp is not None:
    rest_config.regexp = regexp
  if interval is not None:
    rest_config.interval = interval if interval != 0 else None

  checker = Pipe(_as_dict(rest_config), _as_dict(kafka_config))
  checker.loop()


# Site status checker driver
if __name__ == '__main__':
  fire.Fire(check_site)
