import requests
from scapy.all import ARP, Ether, srp
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Hàm quét mạng
def local_network_scan(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc,
            'vendor': get_vendor_by_mac(received.hwsrc)
        })

    return devices

# Hàm lấy vendor theo MAC
def get_vendor_by_mac(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except Exception as e:
        print("Error fetching vendor information:", e)
        return "Unknown"

# Hàm khi nhấn nút Scan
def start_scan():
    ip_range = ip_entry.get()
    if not ip_range:
        messagebox.showwarning("Input Error", "Please enter an IP range!")
        return
    
    scan_button.config(state=tk.DISABLED)
    result_table.delete(*result_table.get_children())  # Clear bảng
    
    # Dùng thread để tránh treo UI
    threading.Thread(target=run_scan, args=(ip_range,)).start()

def run_scan(ip_range):
    devices = local_network_scan(ip_range)
    
    for device in devices:
        result_table.insert("", "end", values=(device['ip'], device['mac'], device['vendor']))
    
    scan_button.config(state=tk.NORMAL)

# UI
root = tk.Tk()
root.title("Network Scanner")

# Khung nhập IP range
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="IP Range (ex: 192.168.1.1/24):").pack(side=tk.LEFT, padx=5)
ip_entry = tk.Entry(frame_input, width=20)
ip_entry.pack(side=tk.LEFT)
ip_entry.insert(0, "192.168.1.1/24")

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=5)

# Bảng kết quả
columns = ("IP Address", "MAC Address", "Vendor")
result_table = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    result_table.heading(col, text=col)
    result_table.column(col, width=200)

result_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Chạy app
root.mainloop()
