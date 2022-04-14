from tkinter import *
import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re

from requests import options

root = Tk()
root.title('Server Dashboard')
root.geometry("640x480+50+50")


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def disks():
    # disk_general = ['disk1_lbl', 'disk2_lbl', 'disk3_lbl', 'disk4_lbl', 'disk5_lbl','disk6_lbl']
    # disk_more = ['disk1_lbl', 'disk2_lbl', 'disk3_lbl', 'disk4_lbl', 'disk5_lbl','disk6_lbl']
    partitions = psutil.disk_partitions()
    # count = 0
    rows1 = 9
    rows2 = 10
    for partition in partitions:
        Label(root, text=f"Device: {partition.device}\nMountpoint: {partition.mountpoint}\nFile system type: {partition.fstype}").grid(row=rows1, column=0, sticky='w')
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        Label(root, text=f"  Total Size: {get_size(psutil.disk_usage(partition.mountpoint).total)}").grid(row=rows2, column=0, sticky='w')
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
        disk_io = psutil.disk_io_counters()
        print(f"Total read: {get_size(disk_io.read_bytes)}")
        print(f"Total write: {get_size(disk_io.write_bytes)}")
        
        rows1 += 2
        rows2 += 2


def net():
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    ##get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")


# 1.Name of the machine 2.Up time 3.IP of the machine
# 4.CPU usage in % 5.CPU temperature 6.RAM usage ?GB/16GB
# 6.Storage (disk space, volume, usage ?GB/1TB)
# 7.Network traffic

uname = platform.uname()
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
cpufreq = psutil.cpu_freq()
svmem = psutil.virtual_memory()

option = ["Genral Info", "CPU", "RAM", "Disk", "Network"]
clicked = StringVar()
clicked.set(option[0])

drop_menu = OptionMenu(root, clicked, *option).grid(row=0, column=1)

system_name_lbl = Label(root, text=f"System: {uname.system}")
node_name_lbl = Label(root, text=f"Node name: {uname.node}")
release_version_lbl = Label(root, text=f"Release version: {uname.release} / {uname.version}")
processor_name_lbl = Label(root, text=f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}")
boot_lbl = Label(root, text=f"Last time it was booted: {bt.day}/{bt.month}/{bt.year} {bt.hour}:{bt.minute}:{bt.second}")
cpu_lbl = Label(root, text=f"CPU usage: {psutil.cpu_percent()}%")
cpufrq_lbl = Label(root, text=f"Current Frequency: {psutil.cpu_freq().min:.2f}Mhz")
ram_lbl = Label(root, text=f"RAM: {get_size(psutil.virtual_memory().used)}/{get_size(psutil.virtual_memory().total)}")
disks()
net()



system_name_lbl.grid(row=1, column=0, sticky='w')
node_name_lbl.grid(row=2, column=0, sticky='w')
release_version_lbl.grid(row=3, column=0, sticky='w')
processor_name_lbl.grid(row=4, column=0, sticky='w')
boot_lbl.grid(row=5, column=0, sticky='w')
cpu_lbl.grid(row=6, column=0, sticky='w')
cpufrq_lbl.grid(row=7, column=0, sticky='w')
ram_lbl.grid(row=8, column=0, sticky='w')
#disk_lbl.grid(row=8, column=0, sticky='w')

def clock():
    cpu = f"CPU usage: {psutil.cpu_percent()}%"
    frq = f"Current Frequency: {psutil.cpu_freq().current:.2f}Mhz"
    ram = f"RAM: {get_size(psutil.virtual_memory().used)}/{get_size(psutil.virtual_memory().total)}"
    cpu_lbl.config(text=cpu)
    ram_lbl.config(text=ram)
    cpufrq_lbl.config(text=frq)
    disks()
    net()
    root.after(750, clock)
clock()



root.mainloop()