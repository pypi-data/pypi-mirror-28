#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/config.py 
@time: 2017/12/16 22:00
"""

import os
import sys


class Config(object):

    def __init__(self, config_dir=None):
        self.config_dir = config_dir
        self.config_filename = 'dops.conf'
        self._loaded_config_file = None

        self.read()

    def config_file_paths(self):

        paths = []

        if self.config_dir:
            paths.append(self.config_dir)

        paths.append(os.path.join(os.path.expanduser('~/.config'), 'dops', self.config_filename))

        return paths

    def read(self):

        for config_file in self.config_file_paths():
            if os.path.exists(config_file):
                try:
                    with open(config_file, encoding='utf-8') as f:
                        pass
                except UnicodeDecodeError as err:
                    sys.exit(1)
                    break
