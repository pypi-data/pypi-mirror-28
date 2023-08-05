#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: /version.py.py
@time: 17-12-26 下午10:14
"""

from . import SubCommand


def _show_version(args):
    try:
        from dops.version import VERSION_INFO
        for name, value in VERSION_INFO:
            print("     {0:10s} :\t{1}".format(name, value))
    except ImportError as e:
        print("get version info failed")


VersionCommand = SubCommand(
    name="version", help="show command version",
    metavar="", func=_show_version
)