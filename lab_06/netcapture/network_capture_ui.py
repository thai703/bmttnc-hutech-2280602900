import subprocess
from scapy.all import sniff, Raw
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

# Lấy danh sách interface (Windows)
def get_interfaces():
    result = subprocess.run(["netsh", "interface", "show", "interface"],
                            capture_output=True, text=True)
    output_lines = result.stdout.splitlines()[3:]
    interfaces = [line.split()[3] for line in output_lines if len(line.split()) >= 4]
    return interfaces

# Hàm xử lý gói tin
def packet_handler(packet):
    if packet.haslayer(Raw):
        log_text.insert(tk.END, f"Captured Packet:\n{str(packet)}\n\n")
        log_text.see(tk.END)

# Hàm khi nhấn Start
def start_capture():
    selected_iface = iface_combo.get()
    if not selected_iface:
        messagebox.showwarning("Input Error", "Please select a network interface!")
        return

    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    log_text.insert(tk.END, f"Starting capture on interface: {selected_iface}\n\n")
    log_text.see(tk.END)

    # Dùng thread để tránh treo UI
    global capture_thread
    capture_thread = threading.Thread(target=run_capture, args=(selected_iface,))
    capture_thread.daemon = True
    capture_thread.start()

# Hàm khi nhấn Stop
def stop_capture():
    global stop_sniff
    stop_sniff = True
    log_text.insert(tk.END, "\nStopping capture...\n")
    log_text.see(tk.END)

# Thực thi sniff
def run_capture(iface):
    global stop_sniff
    stop_sniff = False

    def stop_filter(packet):
        return stop_sniff
    
    sniff(iface=iface, prn=packet_handler, filter="tcp", stop_filter=stop_filter)

    # Sau khi dừng sniff
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    log_text.insert(tk.END, "Capture stopped.\n\n")
    log_text.see(tk.END)

# UI
root = tk.Tk()
root.title("Network Packet Capture")

# Khung chọn interface
frame_iface = tk.Frame(root)
frame_iface.pack(pady=10)

tk.Label(frame_iface, text="Select Network Interface:").pack(side=tk.LEFT, padx=5)
iface_combo = ttk.Combobox(frame_iface, width=30, state="readonly")
iface_combo.pack(side=tk.LEFT)

# Nút Start/Stop
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

start_button = tk.Button(frame_buttons, text="Start Capture", command=start_capture)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(frame_buttons, text="Stop Capture", command=stop_capture, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5)

# Khung log
log_text = scrolledtext.ScrolledText(root, width=100, height=30)
log_text.pack(padx=10, pady=10)

# Khởi tạo danh sách interface
interfaces = get_interfaces()
iface_combo['values'] = interfaces
if interfaces:
    iface_combo.current(0)

# Chạy app
root.mainloop()
