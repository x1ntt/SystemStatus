import psutil
import time
import socket
import requests as req
import json
from collections import OrderedDict

"""
    1. hostname
    2. ip
    3. cpu
    4. mem
    5. disk
    6. 温度
    7. 风扇转速
    8. 网络流量
"""

def find_single_ipv4_address(addrs):
    for addr in addrs:
        if addr.family == socket.AddressFamily.AF_INET:  # IPv4
            return addr.address

def get_ipv4_address(interface_name=None):
    if_addrs = psutil.net_if_addrs()

    if isinstance(interface_name, str) and interface_name in if_addrs:
        addrs = if_addrs.get(interface_name)
        address = find_single_ipv4_address(addrs)
        return address if isinstance(address, str) else ""
    else:
        if_stats = psutil.net_if_stats()
        # remove loopback
        #if_stats_filtered = {key: if_stats[key] for key, stat in if_stats.items() if "loopback" not in stat.flags}
        if_stats_filtered = if_stats
        # sort interfaces by
        # 1. Up/Down
        # 2. Duplex mode (full: 2, half: 1, unknown: 0)
        if_names_sorted = [stat[0] for stat in sorted(if_stats_filtered.items(), key=lambda x: (x[1].isup, x[1].duplex), reverse=True)]
        if_addrs_sorted = OrderedDict((key, if_addrs[key]) for key in if_names_sorted if key in if_addrs)
        for _, addrs in if_addrs_sorted.items():
            address = find_single_ipv4_address(addrs)
            if isinstance(address, str):
                return address
        return ""

def get_disk():
    disks = [ {"path": path, "percent": psutil.disk_usage(path).percent} for path in [p.mountpoint for p in psutil.disk_partitions()]]
    disks = list(filter(lambda x: len(x['path'].split('/')) in [1, 2], disks))
    return disks

def dump_info():
    print (psutil.cpu_times())
    print (psutil.cpu_percent(percpu=False))
    print (psutil.cpu_times_percent())
    print (psutil.cpu_freq(percpu=False))
    print (psutil.net_io_counters(pernic=False, nowrap=True))
    print (get_ipv4_address())
    print (get_disk())
    print ('\n')

def info():
    return {
        "hostname": "123",
        "ip": get_ipv4_address(),
        "cpu": psutil.cpu_percent(percpu=False),
        "mem": psutil.virtual_memory().percent,
        "disk": get_disk()
    }

if __name__ == "__main__":
    while True:
        # dump_info()
        # print (info())
        try:
            data = {"node":json.dumps(info())}
            # print (data)
            req.post("http://192.168.6.170:5000/api/update/node", data=data)
        except Exception as e:
            pass
        time.sleep(1)