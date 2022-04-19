import subprocess
from tkinter import *
import wmi
import sys


BASIC = False
if '-basic' in sys.argv:
    BASIC = True

SIGNAL = False
if '-signal' in sys.argv:
    SIGNAL = True

BASICS = ('SSID', 'Local IP', 'Gateway', 'State', 'Signal')


def retrive_info(x):
    x = x.strip()
    ind = 0
    for i in x:
        if i == ' ':
            break
        ind += 1

    toremv = len(x)-ind
    key = x[:-toremv]

    val = x[24:].strip()
    return key, val


def get_net_info():
    wmi_obj = wmi.WMI()
    try:
        wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
        wmi_out = wmi_obj.query(wmi_sql)
        dev = wmi_out[0]
        gateway = dev.DefaultIPGateway[0]

    except:
        localip = 'Not Found'
        gateway = 'Not Found'
    try:
        localip = dev.IPAddress[0]
    except:
        pass

    NET_INFO = {}
    g = subprocess.getoutput(['netsh', 'wlan', 'show', 'interface']).replace(
        'There is 1 interface on the system:', '')

    info_raw_list = g.split('\n')

    info_list = []

    for i in info_raw_list:
        if i == '' or i == ' ':
            pass
        else:
            info_list.append(i)

    for i in info_list:
        key, val = retrive_info(i)
        NET_INFO[key] = val

    NET_INFO['Gateway'] = gateway
    NET_INFO['Local IP'] = localip
    return NET_INFO


def all_children(root):
    _list = root.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    return _list


def clear_widget(root):
    widget_list = all_children(root)
    for item in widget_list:
        item.grid_forget()


def refresh():
    NET_INFO = get_net_info()
    root.after(400, refresh)
    clear_widget(root)
    if BASIC:
        c = 0
        for i in NET_INFO:
            if i in BASICS:
                Label(text=f'{i}     :      {NET_INFO[i]}').grid(
                    column=1, row=c)
                c += 1
    elif SIGNAL:

        Label(text=NET_INFO['Signal'], font=(
            "Comic Sans MS", 100)).grid(column=0, row=0)
    else:
        c = 0
        for i in NET_INFO:
            Label(text=f'{i}     :      {NET_INFO[i]}').grid(column=1, row=c)
            c += 1


root = Tk()
if BASIC:
    root.geometry('210x110')
refresh()
root.after(400, refresh)
root.title('NetInfo')
root.mainloop()
