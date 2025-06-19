import tkinter as tk
from tkinter import scrolledtext
import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

# Khởi tạo socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
ssl_socket = None  # Chưa kết nối

# Hàm kết nối server
def connect_to_server():
    global ssl_socket
    try:
        ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')
        ssl_socket.connect(server_address)
        log_box.insert(tk.END, "Đã kết nối SSL tới server\n")
        
        # Tạo thread để nhận dữ liệu
        threading.Thread(target=receive_data, daemon=True).start()
    except Exception as e:
        log_box.insert(tk.END, f"Lỗi khi kết nối: {e}\n")

# Hàm ngắt kết nối
def disconnect_from_server():
    global ssl_socket
    if ssl_socket:
        try:
            ssl_socket.close()
            log_box.insert(tk.END, "Đã ngắt kết nối\n")
        except Exception as e:
            log_box.insert(tk.END, f"Lỗi khi ngắt kết nối: {e}\n")

# Hàm gửi message
def send_message():
    msg = message_entry.get()
    if ssl_socket:
        try:
            ssl_socket.send(msg.encode('utf-8'))
            log_box.insert(tk.END, f"Bạn: {msg}\n")
            message_entry.delete(0, tk.END)
        except Exception as e:
            log_box.insert(tk.END, f"Lỗi khi gửi: {e}\n")

# Nhận dữ liệu (thread riêng)
def receive_data():
    global ssl_socket
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            log_box.insert(tk.END, f"Server: {data.decode('utf-8')}\n")
    except Exception as e:
        log_box.insert(tk.END, f"Lỗi khi nhận: {e}\n")

# ==== Giao diện Tkinter ====
root = tk.Tk()
root.title("SSL Client (Tkinter GUI)")

# Log box
log_box = scrolledtext.ScrolledText(root, width=60, height=20)
log_box.pack(padx=10, pady=10)

# Entry nhập message
message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=5)

# Button frame
button_frame = tk.Frame(root)
button_frame.pack()

# Nút kết nối
connect_btn = tk.Button(button_frame, text="Kết nối", command=connect_to_server)
connect_btn.grid(row=0, column=0, padx=5)

# Nút ngắt kết nối
disconnect_btn = tk.Button(button_frame, text="Ngắt kết nối", command=disconnect_from_server)
disconnect_btn.grid(row=0, column=1, padx=5)

# Nút gửi
send_btn = tk.Button(button_frame, text="Gửi", command=send_message)
send_btn.grid(row=0, column=2, padx=5)

# Chạy vòng lặp Tkinter
root.mainloop()
