import tkinter as tk
from tkinter import ttk  # Importing ttk module for themed widgets
import socket
import threading
import random

# Global variable to indicate whether the scanning process should continue or stop
scanning = True

def scan_ports(target, start_port, end_port, open_ports_text, closed_ports_text, network_status_text, progress_bar):
    global scanning
    open_ports_text.delete("1.0", tk.END)
    closed_ports_text.delete("1.0", tk.END)
    progress_bar["value"] = 0  # Reset progress bar
    progress_bar["maximum"] = end_port - start_port + 1
    safe = True
    for port in range(start_port, end_port + 1):
        if not scanning:  # Check if scanning should stop
            break
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    service = socket.getservbyport(port)
                    open_ports_text.insert(tk.END, f"Port {port} ({service}) is open\n")
                    safe = False  # If any port is open, network is considered vulnerable
                else:
                    closed_ports_text.insert(tk.END, f"Port {port} is closed\n")
        except:
            pass
        finally:
            progress_bar["value"] += 1
    
    if scanning:  # Check if scanning was not stopped
        if safe:
            network_status_text.config(text="Network is SAFE", fg="green")
        else:
            network_status_text.config(text="Network is VULNERABLE", fg="red")

def start_scan():
    global scanning
    scanning = True  # Reset scanning flag
    target = target_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    thread = threading.Thread(target=scan_ports, args=(target, start_port, end_port, open_ports_text, closed_ports_text, network_status_text, progress_bar))
    thread.start()

def stop_scan():
    global scanning
    scanning = False  # Set scanning flag to stop the scanning process

def clear_fields():
    target_entry.delete(0, tk.END)
    start_port_entry.delete(0, tk.END)
    end_port_entry.delete(0, tk.END)
    open_ports_text.delete("1.0", tk.END)
    closed_ports_text.delete("1.0", tk.END)
    network_status_text.config(text="")
    progress_bar["value"] = 0

def random_color():
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color

# GUI Setup
root = tk.Tk()
root.title("Network Scanner")
root.geometry("1000x600")  # Increased width
root.configure(bg="#add8e6")  # Light blue background

# Header
header_label = tk.Label(root, text="Network Port Scanner", font=("Helvetica", 20, "bold"), fg="white", bg=random_color())
header_label.pack(pady=(10, 20))

# Definition
definition_label = tk.Label(root, text="A network port scanner is a tool used to discover open and closed ports on a network host.", font=("Helvetica", 12), bg="#add8e6")
definition_label.pack()

# Author
author_label = tk.Label(root, text="Author: Pranjal Usulkar \n Shrilakshmi Doijode", font=("Helvetica", 12), bg="#add8e6", fg="navy")
author_label.pack()

# Target Host
target_frame = tk.Frame(root, bg="#add8e6")
target_frame.pack(pady=10)
target_label = tk.Label(target_frame, text="Target Host:", font=("Helvetica", 14), bg="#add8e6")
target_label.grid(row=0, column=0, padx=(20, 10))
target_entry = tk.Entry(target_frame, font=("Helvetica", 14), width=20)
target_entry.grid(row=0, column=1)

# Port Range
port_frame = tk.Frame(root, bg="#add8e6")
port_frame.pack(pady=10)
start_port_label = tk.Label(port_frame, text="Start Port:", font=("Helvetica", 14), bg="#add8e6")
start_port_label.grid(row=0, column=0, padx=(20, 10))
start_port_entry = tk.Entry(port_frame, font=("Helvetica", 14), width=8)
start_port_entry.grid(row=0, column=1)
end_port_label = tk.Label(port_frame, text="End Port:", font=("Helvetica", 14), bg="#add8e6")
end_port_label.grid(row=0, column=2, padx=(10, 10))
end_port_entry = tk.Entry(port_frame, font=("Helvetica", 14), width=8)
end_port_entry.grid(row=0, column=3)

# Scan Button
scan_button = tk.Button(root, text="Start Scan", font=("Helvetica", 14), command=start_scan, bg=random_color(), fg="white")
scan_button.pack(pady=10)

# Stop Button
stop_button = tk.Button(root, text="Stop Scan", font=("Helvetica", 14), command=stop_scan, bg=random_color(), fg="white")
stop_button.pack(pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=10)

# Open Ports Text with Increased Height and Width, Border, and Auto-Scroll
open_ports_text_frame = tk.Frame(root, bg="#add8e6")
open_ports_text_frame.pack(side=tk.LEFT, padx=10, pady=10)
open_ports_label = tk.Label(open_ports_text_frame, text="Open Ports", font=("Helvetica", 14), bg="#add8e6")
open_ports_label.pack()
open_ports_text = tk.Text(open_ports_text_frame, height=20, width=50, font=("Helvetica", 12), bd=2, relief="solid")
open_ports_text.pack(fill=tk.BOTH, expand=True)
open_ports_scroll = tk.Scrollbar(open_ports_text_frame, command=open_ports_text.yview)
open_ports_scroll.pack(side=tk.RIGHT, fill=tk.Y)
open_ports_text.config(yscrollcommand=open_ports_scroll.set)

# Closed Ports Text with Increased Height and Width, Border, and Auto-Scroll
closed_ports_text_frame = tk.Frame(root, bg="#add8e6")
closed_ports_text_frame.pack(side=tk.LEFT, padx=10, pady=10)
closed_ports_label = tk.Label(closed_ports_text_frame, text="Closed Ports", font=("Helvetica", 14), bg="#add8e6")
closed_ports_label.pack()
closed_ports_text = tk.Text(closed_ports_text_frame, height=20, width=50, font=("Helvetica", 12), bd=2, relief="solid")
closed_ports_text.pack(fill=tk.BOTH, expand=True)
closed_ports_scroll = tk.Scrollbar(closed_ports_text_frame, command=closed_ports_text.yview)
closed_ports_scroll.pack(side=tk.RIGHT, fill=tk.Y)
closed_ports_text.config(yscrollcommand=closed_ports_scroll.set)

# Network Status Text
network_status_text = tk.Label(root, text="", font=("Helvetica", 14), bg="#add8e6", fg="black")
network_status_text.pack()

# Clear Button
clear_button = tk.Button(root, text="Clear Fields", font=("Helvetica", 14), command=clear_fields, bg=random_color(), fg="white")
clear_button.pack(pady=10)

root.mainloop()
