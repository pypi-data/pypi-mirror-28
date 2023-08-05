#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/get.py 
@time: 2017/12/27 23:18
"""

from . import BaseFlag, SubCommand
from dops.plugins.node import NodeInfo
from dops.core.logger import logger


def _get_system(args):
    n = NodeInfo()
    if args.t is None:
        args.t = "json"
    logger.info("start get {} --full={} -t={}".format(args.name, args.full, args.t if None else "json"))
    return n.get_system(args)

GetCommand = SubCommand(
    name="get", help="get the resource", metavar="<resource>",
    flags=[],
    subcmds=[
        SubCommand(
            name="system", usage="get system info",
            flags=[
                BaseFlag('name', metavar="name", help="eg:cpu,mem,disk", nargs='?'),
                BaseFlag('--full', action='store_true', help="all info"),
                BaseFlag('-t', choices=('table', 'json'), help="default json"),
            ],
            func=_get_system
        ),
    ]
)

