#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/system.py 
@time: 2017/12/30 12:42
"""

import os
import psutil
import time
import datetime
import platform
import socket
import json
from dops.core.logger import logger


def socket_constants(prefix):
    return dict((getattr(socket, n), n) for n in dir(socket) if n.startswith(prefix))

socket_families = socket_constants('AF_')
socket_types = socket_constants('SOCK_')


class SystemInfo(object):

    def _uptime(self, boot_time=False):
        uptime_simple = int(time.time() - psutil.boot_time())
        if boot_time:
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            m, s = divmod(uptime_simple, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            if uptime_simple <= 86400:
                return "{},up {}:{}".format(boot_time, h, m)
            else:
                return "{}, up {:>2} days {:>2}:{:>2}".format(boot_time, d, h, m)
        return "{}".format(uptime_simple)

    def _get_cpu_num(self):
        return "{}/{}".format(psutil.cpu_count(),psutil.cpu_count(logical=True))

    def get_sysinfo(self):
        sysinfo = {
            'os': platform.platform(),
            'uptime': self._uptime(boot_time=True),
            'hostname': socket.gethostname(),

            'load_avg': os.getloadavg(),
            'cpus[p/l]': self._get_cpu_num(),
            'memory': "{} M".format(self.get_memory()['total']/1024/1024)
        }
        return sysinfo

    def get_memory(self):
        return psutil.virtual_memory()._asdict()

    def get_swap_space(self):
        sm = psutil.swap_memory()
        swap = {
            'total': sm.total,
            'free': sm.free,
            'used': sm.used,
            'percent': sm.percent,
            'swapped_in': sm.sin,
            'swapped_out': sm.sout
        }
        return swap

    def get_cpu(self):
        return psutil.cpu_times_percent(0)._asdict()

    def get_cpu_cores(self):
        return [c._asdict() for c in psutil.cpu_times_percent(0, percpu=True)]

    def get_disks(self, all_partitions=False):
        disks = []
        for dp in psutil.disk_partitions(all_partitions):
            usage = psutil.disk_usage(dp.mountpoint)
            disk = {
                'device': dp.device,
                'mountpoint': dp.mountpoint,
                'type': dp.fstype,
                'options': dp.opts,
                'space_total': usage.total,
                'space_used': usage.used,
                'space_used_percent': usage.percent,
                'space_free': usage.free
            }
            disks.append(disk)

        return disks

    def get_disks_counters(self, perdisk=True):
        return dict((dev, c._asdict()) for dev, c in psutil.disk_io_counters(perdisk=perdisk).iteritems())

    def get_users(self):
        return [u._asdict() for u in psutil.users()]

    def get_process_list(self):
        process_list = []
        for p in psutil.process_iter():
            mem = p.memory_info()

            # psutil throws a KeyError when the uid of a process is not associated with an user.
            try:
                username = p.username()
            except KeyError:
                username = None

            proc = {
                'pid': p.pid,
                'name': p.name(),
                'cmdline': ' '.join(p.cmdline()),
                'user': username,
                'status': p.status(),
                'created': p.create_time(),
                'mem_rss': mem.rss,
                'mem_vms': mem.vms,
                'mem_percent': p.memory_percent(),
                'cpu_percent': p.cpu_percent(0)
            }
            process_list.append(proc)

        return process_list

    def get_process(self, pid):
        p = psutil.Process(pid)
        mem = p.memory_info_ex()
        cpu_times = p.cpu_times()

        # psutil throws a KeyError when the uid of a process is not associated with an user.
        try:
            username = p.username()
        except KeyError:
            username = None

        return {
            'pid': p.pid,
            'ppid': p.ppid(),
            'parent_name': p.parent().name() if p.parent() else '',
            'name': p.name(),
            'cmdline': ' '.join(p.cmdline()),
            'user': username,
            'uid_real': p.uids().real,
            'uid_effective': p.uids().effective,
            'uid_saved': p.uids().saved,
            'gid_real': p.gids().real,
            'gid_effective': p.gids().effective,
            'gid_saved': p.gids().saved,
            'status': p.status(),
            'created': p.create_time(),
            'terminal': p.terminal(),
            'mem_rss': mem.rss,
            'mem_vms': mem.vms,
            'mem_shared': mem.shared,
            'mem_text': mem.text,
            'mem_lib': mem.lib,
            'mem_data': mem.data,
            'mem_dirty': mem.dirty,
            'mem_percent': p.memory_percent(),
            'cwd': p.cwd(),
            'nice': p.nice(),
            'io_nice_class': p.ionice()[0],
            'io_nice_value': p.ionice()[1],
            'cpu_percent': p.cpu_percent(0),
            'num_threads': p.num_threads(),
            'num_files': len(p.open_files()),
            'num_children': len(p.children()),
            'num_ctx_switches_invol': p.num_ctx_switches().involuntary,
            'num_ctx_switches_vol': p.num_ctx_switches().voluntary,
            'cpu_times_user': cpu_times.user,
            'cpu_times_system': cpu_times.system,
            'cpu_affinity': p.cpu_affinity()
        }

    def get_process_limits(self, pid):
        p = psutil.Process(pid)
        return {
            'RLIMIT_AS': p.rlimit(psutil.RLIMIT_AS),
            'RLIMIT_CORE': p.rlimit(psutil.RLIMIT_CORE),
            'RLIMIT_CPU': p.rlimit(psutil.RLIMIT_CPU),
            'RLIMIT_DATA': p.rlimit(psutil.RLIMIT_DATA),
            'RLIMIT_FSIZE': p.rlimit(psutil.RLIMIT_FSIZE),
            'RLIMIT_LOCKS': p.rlimit(psutil.RLIMIT_LOCKS),
            'RLIMIT_MEMLOCK': p.rlimit(psutil.RLIMIT_MEMLOCK),
            'RLIMIT_MSGQUEUE': p.rlimit(psutil.RLIMIT_MSGQUEUE),
            'RLIMIT_NICE': p.rlimit(psutil.RLIMIT_NICE),
            'RLIMIT_NOFILE': p.rlimit(psutil.RLIMIT_NOFILE),
            'RLIMIT_NPROC': p.rlimit(psutil.RLIMIT_NPROC),
            'RLIMIT_RSS': p.rlimit(psutil.RLIMIT_RSS),
            'RLIMIT_RTPRIO': p.rlimit(psutil.RLIMIT_RTPRIO),
            'RLIMIT_RTTIME': p.rlimit(psutil.RLIMIT_RTTIME),
            'RLIMIT_SIGPENDING': p.rlimit(psutil.RLIMIT_SIGPENDING),
            'RLIMIT_STACK': p.rlimit(psutil.RLIMIT_STACK)
        }

    def get_process_environment(self, pid):
        with open('/proc/%d/environ' % pid) as f:
            contents = f.read()
            env_vars = dict(row.split('=', 1) for row in contents.split('\0') if '=' in row)
        return env_vars

    def get_process_threads(self, pid):
        threads = []
        proc = psutil.Process(pid)
        for t in proc.threads():
            thread = {
                'id': t.id,
                'cpu_time_user': t.user_time,
                'cpu_time_system': t.system_time,
            }
            threads.append(thread)
        return threads

    def get_process_open_files(self, pid):
        proc = psutil.Process(pid)
        return [f._asdict() for f in proc.open_files()]

    def get_process_connections(self, pid):
        proc = psutil.Process(pid)
        connections = []
        for c in proc.connections(kind='all'):
            conn = {
                'fd': c.fd,
                'family': socket_families[c.family],
                'type': socket_types[c.type],
                'local_addr_host': c.laddr[0] if c.laddr else None,
                'local_addr_port': c.laddr[1] if c.laddr else None,
                'remote_addr_host': c.raddr[0] if c.raddr else None,
                'remote_addr_port': c.raddr[1] if c.raddr else None,
                'state': c.status
            }
            connections.append(conn)

        return connections

    def get_process_memory_maps(self, pid):
        return [m._asdict() for m in psutil.Process(pid).memory_maps()]

    def get_process_children(self, pid):
        proc = psutil.Process(pid)
        children = []
        for c in proc.children():
            child = {
                'pid': c.pid,
                'name': c.name(),
                'cmdline': ' '.join(c.cmdline()),
                'status': c.status()
            }
            children.append(child)

        return children

    def get_connections(self, filters=None):
        filters = filters or {}
        connections = []

        for c in psutil.net_connections('all'):
            conn = {
                'fd': c.fd,
                'pid': c.pid,
                'family': socket_families[c.family],
                'type': socket_types[c.type],
                'local_addr_host': c.laddr[0] if c.laddr else None,
                'local_addr_port': c.laddr[1] if c.laddr else None,
                'remote_addr_host': c.raddr[0] if c.raddr else None,
                'remote_addr_port': c.raddr[1] if c.raddr else None,
                'state': c.status
            }

            for k, v in filters.iteritems():
                if v and conn.get(k) != v:
                    break
            else:
                connections.append(conn)

        return connections


s = SystemInfo()


class NodeInfo(object):

    def _output_fmt(self, func, t=None, nsp=None):
        _info_output_fmt = '{0:>10s}:\t{1}'
        if func == "nsp":
            return _info_output_fmt.format(nsp if None else "None", "not support now.")
        if t == "json":
            return json.dumps(func)
        else:
            for (k, v) in func.items():
                print(_info_output_fmt.format(k, v))

    def get_system(self, args):
        logger.info("end get {} --full={} -t={}".format(args.name, args.full, args.t if None else "json"))
        if args.full or args.name is None:
            return self._output_fmt(s.get_sysinfo(), args.t)
        elif args.name == "cpu":
            return self._output_fmt(s.get_cpu(), args.t)
        elif args.name == "mem":
            return self._output_fmt(s.get_memory(), args.t)
        elif args.name == "disk":
            return self._output_fmt(s.get_disks(), args.t)
        else:
            return self._output_fmt("nsp", args.t, nsp=args.name)


