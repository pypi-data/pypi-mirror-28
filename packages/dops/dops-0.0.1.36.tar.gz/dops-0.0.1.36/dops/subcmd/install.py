#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/install.py 
@time: 2018/1/3 23:43
"""

from dops.core.install import GeneralInstall, NetworkInstall
from . import BaseFlag, SubCommand


def _create_instance(args):
    m = GeneralInstall()
    return m.install_instance(args.name, args.reinstall)

def _create_network(args):
    m = NetworkInstall()
    return m.run()

InstallCommand = SubCommand(
    name="install", help="install instance", metavar="<resource>",
    flags=[],
    subcmds=[
        SubCommand(
            name='network',
            usage='install network',
            func=_create_network
        ),
        SubCommand(
            name="instance",
            usage="install an instance",
            flags=[
                BaseFlag('name', metavar='instance_id'),
                BaseFlag('-r', '--reinstall', action='store_true')
            ],
            func=_create_instance
        ),
    ]
)