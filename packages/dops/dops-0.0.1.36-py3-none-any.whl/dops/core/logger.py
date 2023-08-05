#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/logs.py 
@time: 2017/12/16 23:46
"""

import os
import json
import logging
import platform
import logging.config

system = platform.system().lower()

if system == 'darwin':
    LOG_FILE = '/tmp/dops.log'
else:
    LOG_FILE = '/var/log/dops.log'


LOGGING_CFG = {
    "version": 1,
    "disable_existing_loggers": "False",
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"]
    },
    "formatters": {
        "standard": {
            "format": "%(asctime)s -- %(levelname)s -- %(message)s"
        },
        "short": {
            "format": "%(levelname)s: %(message)s"
        },
        "free": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "standard",
            "when": "midnight",
            "interval":1,
            "backupCount":30,
            "filename": LOG_FILE
        },
        "console": {
            "level": "CRITICAL",
            "class": "logging.StreamHandler",
            "formatter": "free"
        }
    },
    "loggers": {
        "debug": {
            "handlers": ["file", "console"],
            "level": "DEBUG"
        },
        "verbose": {
            "handlers": ["file", "console"],
            "level": "INFO"
        },
        "standard": {
            "handlers": ["file"],
            "level": "INFO"
        },
        "requests": {
            "handlers": ["file", "console"],
            "level": "ERROR"
        },
        "elasticsearch": {
            "handlers": ["file", "console"],
            "level": "ERROR"
        },
        "elasticsearch.trace": {
            "handlers": ["file", "console"],
            "level": "ERROR"
        }
    }
}


def dops_logger(env_key='LOG_CFG'):

    _logger = logging.getLogger()

    config = LOGGING_CFG
    user_file = os.getenv(env_key, None)
    if user_file and os.path.exists(user_file):
        with open(user_file, 'r') as f:
            config = json.load(f)

    logging.config.dictConfig(config)

    return _logger

logger = dops_logger()
