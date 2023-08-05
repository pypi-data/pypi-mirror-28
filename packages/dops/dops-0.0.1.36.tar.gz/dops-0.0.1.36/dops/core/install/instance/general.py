#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/general.py.py 
@time: 2018/1/3 23:56
"""

from dops.core.install.base import BaseInstall


class GeneralInstall(BaseInstall):
    def install_instance(self, instance_id, reinstall=False):
        if not reinstall:
            print("install {} ok!!!".format(instance_id))
        else:
            print("reinstall {} ok!!!".format(instance_id))
