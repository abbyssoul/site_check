#!/usr/bin/env python3
"""
 CLI driver used for controlling web-site status recorder
"""

import fire
import logging

from check_persister import Pipe
import kafka_config
import db_config


def _as_dict(module):
    return {setting: getattr(module, setting) for setting in dir(module) if not setting.startswith('_')}


def record_status():
  logging.basicConfig(level=logging.INFO)

  recorder = Pipe(source_config=_as_dict(kafka_config),
                  sink_config=_as_dict(db_config))
  recorder.loop()


# Site status checker driver
if __name__ == '__main__':
    fire.Fire(record_status)
