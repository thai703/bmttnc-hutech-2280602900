import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    """Hàm chạy trên một luồng riêng để lắng nghe dữ liệu từ server."""
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            # Dùng \r để ghi đè dòng nhập liệu hiện tại
            print(f"\rNhận: {data.decode('utf-8')}\nNhập tin nhắn: ", end="")
    except ssl.SSLError:
        print("\rLỗi SSL. Kết nối có thể đã bị đóng.")
    except Exception:
        # Bỏ qua lỗi khi socket đã bị đóng ở luồng chính
        pass
    finally:
        print("\rĐã ngắt kết nối với server.")
        

# --- Phần chính của client ---

# Tạo socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tạo SSL context
# PROTOCOL_TLS_CLIENT là lựa chọn tốt hơn cho phía client
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) 

# Vì chúng ta đang dùng chứng chỉ tự ký (self-signed), 
# client cần được cấu hình để không xác thực nó.
# TRONG THỰC TẾ, ĐÂY LÀ MỘT RỦI RO BẢO MẬT.
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Bọc socket client với SSL
ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')
ssl_socket.connect(server_address)
print("Đã kết nối SSL tới server.")

# Bắt đầu một luồng để nhận dữ liệu từ server
receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
receive_thread.start()

# Gửi dữ liệu lên server từ luồng chính
try:
    while True:
        message = input("Nhập tin nhắn: ")
        if message.lower() == 'exit':
            break
        ssl_socket.send(message.encode('utf-8'))
except KeyboardInterrupt:
    print("\nĐang đóng kết nối...")
finally:
    # Đóng socket để luồng nhận cũng kết thúc
    ssl_socket.close()