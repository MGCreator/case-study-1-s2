import psutil
from tkinter import *

root = Tk()
frame_genral = Frame(root, bg="grey")
frame_genral.grid(row=0, column=0)

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



ram_lbl = Label(frame_genral, text=f"RAM Used/Total: {get_size(psutil.virtual_memory().used)}/{get_size(psutil.virtual_memory().total)}")
ram_free_lbl = Label(frame_genral, text=f"RAM Available:: {get_size(psutil.virtual_memory().free)}")
ram_used_in_percent_lbl = Label(frame_genral, text=f"RAM Used in %: {get_size(psutil.virtual_memory().percent)}%")

ram_lbl.grid(row=1, column=0, sticky='w')
ram_free_lbl.grid(row=2, column=0, sticky='w')
ram_used_in_percent_lbl.grid(row=3, column=0, sticky='w')


def clock():
        ram = f"RAM Used/Total: {get_size(psutil.virtual_memory().used)}/{get_size(psutil.virtual_memory().total)}"
        ram_free = f"RAM Available: {get_size(psutil.virtual_memory().free)}"
        ram_used = f"RAM Used in %: {get_size(psutil.virtual_memory().percent)}%"
        ram_lbl.config(text=ram)
        ram_free_lbl.config(text=ram_free)
        ram_used_in_percent_lbl.config(text=ram_used)
        root.after(750, clock)
clock()

root.mainloop()