#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/__init__.py 
@time: 2018/1/15 00:08
"""

import ipaddress
from dops.core.install.base import BaseInstall


class NetworkInstall(BaseInstall):

    def choose_network(self, ipv4addr):
        pass

    def auto_choose_network(self, node_ipv4):
        pass

    def do_install_calico(self, nodes):
        if nodes is None:
            print('install calico')
        return 0

    def re_install_manage(self):
        pass

    def determine(self):
        network_mode = 'calico'
        nodes = None
        return network_mode, nodes

    def run(self):
        network_mode, nodes = self.determine()
        if network_mode == 'calico':
            result = self.do_install_calico(nodes)
        else:
            pass

        return result
