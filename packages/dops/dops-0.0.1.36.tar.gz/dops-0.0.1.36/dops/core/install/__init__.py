#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/__init__.py.py 
@time: 2018/1/15 00:05
"""

from .instance.general import GeneralInstall
from .network import NetworkInstall


__all__ = ('GeneralInstall', 'NetworkInstall')