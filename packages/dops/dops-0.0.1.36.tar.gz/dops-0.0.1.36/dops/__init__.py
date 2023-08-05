#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/__init__.py 
@time: 2017/12/16 21:52
"""


import sys
import locale
import argparse
import platform
from dops.core.logger import logger
from dops.subcmd import VersionCommand, GetCommand, InstallCommand
from dops.version import VERSION_INFO


__version__ = dict(VERSION_INFO)['pypi']
__author__ = 'ysicing <ops.ysicing@gmail.com>'
__license__ = 'LGPLv3'


# Check locale
try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    print("Warning: Unable to set locale. Expect encoding problems.")

try:
    from psutil import __version__ as psutil_version
except ImportError:
    print('PSutil library not found.Dops will exit')
    sys.exit(1)


class SubCommands(object):

    @classmethod
    def add(cls, subparsers, *subcmds):
        for subcmd in subcmds:
            p = subparsers.add_parser(subcmd.name, help=subcmd.help)
            for flag in subcmd.flags:
                p.add_argument(*flag.args, **flag.kwargs)
            p.set_defaults(func=subcmd.func, usage=subcmd.usage)
            if subcmd.subcmds:
                cls.add(p.add_subparsers(metavar=subcmd.metavar), *subcmd.subcmds)


def main():

    logger.info('Start dops {}'.format(__version__))
    logger.info('{} {} and Psutil {} detected'.format(
        platform.python_implementation(),
        platform.python_version(),
        psutil_version
    ))
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(metavar='<subcommand>')
    SubCommands.add(subparsers, VersionCommand, GetCommand, InstallCommand)
    args = parser.parse_args()

    if hasattr(args, 'func') and args.func is not None:
        return args.func(args)
    else:
        parser.print_help()