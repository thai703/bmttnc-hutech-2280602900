import socket
from scapy.all import IP, TCP, sr1, send
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389]

# Hàm quét
def scan_common_ports(target_domain, timeout=2):
    open_ports = []
    try:
        target_ip = socket.gethostbyname(target_domain)
    except Exception as e:
        messagebox.showerror("Error", f"Could not resolve domain: {e}")
        return open_ports

    log_text.insert(tk.END, f"Scanning {target_ip} ({target_domain})...\n")
    log_text.see(tk.END)

    for port in COMMON_PORTS:
        response = sr1(IP(dst=target_ip)/TCP(dport=port, flags="S"),
                       timeout=timeout, verbose=0)

        if response and response.haslayer(TCP) and response[TCP].flags == 0x12:
            open_ports.append(port)
            send(IP(dst=target_ip)/TCP(dport=port, flags="R"), verbose=0)

            log_text.insert(tk.END, f"[OPEN] Port {port}\n")
            log_text.see(tk.END)
        else:
            log_text.insert(tk.END, f"[CLOSED] Port {port}\n")
            log_text.see(tk.END)
    
    return open_ports

# Hàm khi nhấn nút
def start_scan():
    target_domain = target_entry.get()
    if not target_domain:
        messagebox.showwarning("Input Error", "Please enter a target domain/IP!")
        return

    scan_button.config(state=tk.DISABLED)
    log_text.delete(1.0, tk.END)

    threading.Thread(target=run_scan, args=(target_domain,)).start()

def run_scan(target_domain):
    open_ports = scan_common_ports(target_domain)

    if open_ports:
        log_text.insert(tk.END, f"\nScan complete. Open ports: {open_ports}\n")
    else:
        log_text.insert(tk.END, "\nScan complete. No open common ports found.\n")

    scan_button.config(state=tk.NORMAL)

# UI
root = tk.Tk()
root.title("Common Port Scanner")

# Khung nhập target
frame_target = tk.Frame(root)
frame_target.pack(pady=10)

tk.Label(frame_target, text="Target domain/IP:").pack(side=tk.LEFT, padx=5)
target_entry = tk.Entry(frame_target, width=30)
target_entry.pack(side=tk.LEFT)
target_entry.insert(0, "127.0.0.1")

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=5)

# Khung log
log_text = scrolledtext.ScrolledText(root, width=80, height=25)
log_text.pack(padx=10, pady=10)

# Chạy app
root.mainloop()
