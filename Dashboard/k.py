from datetime import date, datetime
import matplotlib.pyplot as plt

import matplotlib.animation as animation
import psutil
import numpy as np

e = datetime.now()

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

time = 0
print("speedtest-cli --json --secure >> ok.json")
#z = [psutil.net_io_counters().bytes_recv]
fig = plt.figure()
ax = fig.add_subplot()
yar = []


def update(i):
    #plt.clear()
    #ax.set_xlim([20, 60])
    
    x = [get_size(psutil.net_io_counters().bytes_sent)]
    y = psutil.cpu_percent()
    yar.append(y)
    ax.clear()
    ax.plot(yar)
    time_len = len(yar)
    plt.title("CPU Usage")
    plt.xlabel("Time 60s")
    plt.ylabel("Usage in %")
    ax.set_ylim([0, 100])
    if time_len == 60:
        yar.pop(0)
    # for i in range(len(yar)):
    #     print("xar " + str(x))
    #     print("yar " + str(e.second))
    

ani = animation.FuncAnimation(fig,update, interval=1000)

plt.show()