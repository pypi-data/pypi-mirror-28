# coding=UTF-8
import logging
import os
import platform
import psutil
import socket
import time

# from .helpers import socket_families, socket_types
# from .net import get_interface_addresses, NetIOCounters
# from log.log import Logs
# from .heartbeat import HeartBeat


class SystemInfo(object):

    def __init__(self):
        # self.logs = Logs()
        # self.net_io_counters = NetIOCounters()
        # self.heartbeat = HeartBeat()
        pass

    @staticmethod
    def get_system_info():
        uptime = int(time.time() - psutil.boot_time())

        sys_info = {
            'uptime': uptime,
            'hostname': socket.gethostname(),
            'os': platform.platform(),
            'load_avg': psutil.cpu_times_percent(),
            'num_cpus': psutil.cpu_count()
        }

        return sys_info

    @staticmethod
    def get_memory():
        return psutil.virtual_memory()

    @staticmethod
    def get_swap_space():
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

    @staticmethod
    def get_cpu():
        return psutil.cpu_times_percent()._asdict()

    @staticmethod
    def get_cpu_temp():
        return 1

    @staticmethod
    def get_disks(all_partitions=False):
        disks = []

        for dp in psutil.disk_partitions(all_partitions):
            usage = psutil.disk_usage(dp.mountpoint)

            disk = {
                'device': dp.device,
                'mount_point': dp.mountpoint,
                'type': dp.fstype,
                'options': dp.opts,
                'space_total': usage.total,
                'space_used': usage.used,
                'space_used_percent': usage.percent,
                'space_free': usage.free
            }

            disks.append(disk)

        return disks

    @staticmethod
    def get_process_list():
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

    @staticmethod
    def get_process(pid):
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

    @staticmethod
    def get_process_environment(pid):
        with open('/proc/%d/environ' % pid) as f:
            contents = f.read()
            env_vars = dict(row.split('=', 1) for row in contents.split('\0') if '=' in row)
        return env_vars

    @staticmethod
    def get_process_threads(pid):
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

    # def get_slave_status(self):
    #     return self.heartbeat.slave_status

    # def get_logs(self):
    #     available_logs = []
    #
    #     for log in self.logs.get_available():
    #
    #         try:
    #             stat = os.stat(log.filename)
    #             available_logs.append({
    #                 'path': log.filename.encode("utf-8"),
    #                 'size': stat.st_size,
    #                 'atime': stat.st_atime,
    #                 'mtime': stat.st_mtime
    #             })
    #         except OSError:
    #             logger.info('Could not stat "%s", removing from available logs', log.filename)
    #             self.logs.remove_available(log.filename)
    #
    #     return available_logs
    #
    # def read_log(self, filename, session_key=None, seek_tail=False):
    #     log = self.logs.get(filename, key=session_key)
    #
    #     if seek_tail:
    #         log.set_tail_position()
    #
    #     return log.read()
    #
    # def search_log(self, filename, text, session_key=None):
    #     log = self.logs.get(filename, key=session_key)
    #     pos, bufferpos, res = log.search(text)
    #     stat = os.stat(log.filename)
    #
    #     data = {
    #         'position': pos,
    #         'buffer_pos': bufferpos,
    #         'filesize': stat.st_size,
    #         'content': res
    #     }
    #
    #     return data
