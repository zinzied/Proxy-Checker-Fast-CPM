# -*- coding: utf-8 -*-
"""
Proxy Checker Script

Author: Zied Boughdir
Date: 2024-07-10
Description: This script checks the availability of proxies and categorizes them as working or dead.
"""

import urllib.request as urllib2  # Network lib
import threading  # Threading lib
import socket  # Socket lib
import sys  # System lib
import time  # Time lib
import os  # Os lib
from struct import pack  # For packing data
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Don't create .pyc
sys.dont_write_bytecode = True

# Colours
red = "red"
green = "green"
yellow = "yellow"
blue = "blue"
defcol = "black"

def log_message(msg, color=defcol):
    log_text.insert(tk.END, msg + "\n", color)
    log_text.see(tk.END)

def error(msg):
    log_message("[!] - " + msg, red)

def alert(msg):
    log_message("[#] - " + msg, blue)

def action(msg):
    log_message("[+] - " + msg, green)

def errorExit(msg):
    sys.exit("[!] - Fatal - " + msg)

def get(text):
    return input("[#] - " + text)

def saveToFile(proxy):
    with open(outputfile, 'a') as file:
        file.write(proxy + "\n")

def isSocks(host, port, soc):
    proxy = host + ":" + port
    try:
        if socks5(host, port, soc):
            action("%s is socks5." % proxy)
            return True
        if socks4(host, port, soc):
            action("%s is socks4." % proxy)
            return True

    except socket.timeout:
        alert("Timeout during socks check: " + proxy)
        return False
    except socket.error:
        alert("Connection refused during socks check: " + proxy)
        return False

def socks4(host, port, soc):  # Check if a proxy is Socks4 and alive
    ipaddr = socket.inet_aton(host)
    packet4 = b"\x04\x01" + pack(">H", int(port)) + ipaddr + b"\x00"
    soc.sendall(packet4)
    data = soc.recv(8)
    if len(data) < 2:
        # Null response
        return False
    if data[0] != 0:
        # Bad data
        return False
    if data[1] != 0x5A:
        # Server returned an error
        return False
    return True

def socks5(host, port, soc):  # Check if a proxy is Socks5 and alive
    soc.sendall(b"\x05\x01\x00")
    data = soc.recv(2)
    if len(data) < 2:
        # Null response
        return False
    if data[0] != 5:
        # Not socks5
        return False
    if data[1] != 0:
        # Requires authentication
        return False
    return True

def isAlive(pip, timeout):  # Check if a proxy is alive
    try:
        proxy_handler = urllib2.ProxyHandler({'http': pip})  # Setup proxy handler
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]  # Some headers
        urllib2.install_opener(opener)  # Install the opener
        req = urllib2.Request('http://www.google.com')  # Make the request
        sock = urllib2.urlopen(req, None, timeout=timeout)  # Open url
    except urllib2.HTTPError as e:  # Catch exceptions
        error(pip + " throws: " + str(e.code))
        return False
    except Exception as details:
        error(pip + " throws: " + str(details))
        return False
    return True

def checkProxies():
    global dead_proxies_count, working_proxies_count
    while len(toCheck) > 0 and not stop_flag:
        proxy = toCheck[0]
        toCheck.pop(0)
        alert("Checking %s" % proxy)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        host = proxy.split(":")[0]
        port = proxy.split(":")[1]
        if int(port) < 0 or int(port) > 65536:
            error("Invalid port for " + proxy)
            continue
        if isSocks(host, port, s):
            socks.append(proxy)
            saveToFile(proxy)
            working_proxies_count += 1
        else:
            alert("%s not a working socks 4/5." % proxy)
            if isAlive(proxy, timeout):
                action("Working http/https proxy found (%s)!" % proxy)
                working.append(proxy)
                saveToFile(proxy)
                working_proxies_count += 1
            else:
                error("%s not working." % proxy)
                dead_proxies_count += 1
        s.close()
        update_progress()
        update_counters()

def start_checking():
    global proxiesfile, outputfile, threadsnum, timeout, toCheck, checking, stop_flag, dead_proxies_count, working_proxies_count

    proxiesfile = proxy_list_entry.get()
    outputfile = output_file_entry.get()
    threadsnum = int(threads_entry.get())
    timeout = int(timeout_entry.get())

    try:
        proxiesfile = open(proxiesfile, "r")
    except:
        messagebox.showerror("Error", "Unable to open file: %s" % proxiesfile)
        return

    for line in proxiesfile.readlines():
        toCheck.append(line.strip('\n'))
    proxiesfile.close()

    if os.path.isfile(outputfile):
        check = messagebox.askyesno("Warning", "Output file already exists, content will be overwritten! Continue?")
        if not check:
            messagebox.showinfo("Info", "Quitting...")
            return

    progress_bar['maximum'] = len(toCheck)

    stop_flag = False
    dead_proxies_count = 0
    working_proxies_count = 0
    for i in range(threadsnum):
        threads.append(threading.Thread(target=checkProxies))
        threads[i].setDaemon(True)
        action("Starting thread n: " + str(i + 1))
        threads[i].start()
        time.sleep(0.25)

    action(str(threadsnum) + " threads started...")
    checking = True
    monitor_threads()

def monitor_threads():
    global checking
    if checking:
        if len(threading.enumerate()) - 1 == 0:
            alert("All threads done.")
            action(str(len(working)) + " alive proxies.")
            action(str(len(socks)) + " socks proxies.")
            action(str(len(socks) + len(working)) + " total alive proxies.")
            checking = False
        else:
            alert(str(len(working)) + " alive proxies until now.")
            alert(str(len(socks)) + " socks proxies until now.")
            alert(str(len(toCheck)) + " remaining proxies.")
            alert(str(len(threading.enumerate()) - 1) + " active threads.")
        root.after(5000, monitor_threads)

def update_progress():
    progress_bar['value'] = progress_bar['maximum'] - len(toCheck)
    root.update_idletasks()

def update_counters():
    dead_proxies_label.config(text=f"Dead Proxies: {dead_proxies_count}")
    working_proxies_label.config(text=f"Working Proxies: {working_proxies_count}")

def start_thread():
    threading.Thread(target=start_checking).start()

def stop_checking():
    global stop_flag
    stop_flag = True
    action("Stopping all threads...")

socks = []
working = []
toCheck = []
threads = []
checking = True
stop_flag = False
dead_proxies_count = 0
working_proxies_count = 0

# GUI setup
root = tk.Tk()
root.title("Proxy Checker")

# Apply a theme
style = ttk.Style(root)
style.theme_use('alt')  # You can try 'clam', 'alt', 'default', 'classic'

# Customize the theme
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12), padding=5)
style.configure('TEntry', font=('Helvetica', 12))
style.configure('TProgressbar', thickness=20)

tk.Label(root, text="Proxy list:").grid(row=0, column=0, padx=10, pady=5)
proxy_list_entry = ttk.Entry(root, width=50)
proxy_list_entry.grid(row=0, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=lambda: proxy_list_entry.insert(0, filedialog.askopenfilename())).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Output file:").grid(row=1, column=0, padx=10, pady=5)
output_file_entry = ttk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=lambda: output_file_entry.insert(0, filedialog.asksaveasfilename())).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Number of threads:").grid(row=2, column=0, padx=10, pady=5)
threads_entry = ttk.Entry(root, width=50)
threads_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Timeout (seconds):").grid(row=3, column=0, padx=10, pady=5)
timeout_entry = ttk.Entry(root, width=50)
timeout_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Button(root, text="Start", command=start_thread).grid(row=4, column=1, padx=10, pady=20)
ttk.Button(root, text="Stop", command=stop_checking).grid(row=4, column=2, padx=10, pady=20)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=20)

log_text = tk.Text(root, height=15, width=80)
log_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Adding tags for colors
log_text.tag_config("red", foreground="red")
log_text.tag_config("green", foreground="green")
log_text.tag_config("yellow", foreground="yellow")
log_text.tag_config("blue", foreground="blue")
log_text.tag_config("black", foreground="black")

# Add labels for counters
dead_proxies_label = ttk.Label(root, text="Dead Proxies: 0")
dead_proxies_label.grid(row=7, column=0, padx=10, pady=5)

working_proxies_label = ttk.Label(root, text="Working Proxies: 0")
working_proxies_label.grid(row=7, column=1, padx=10, pady=5)

root.mainloop()