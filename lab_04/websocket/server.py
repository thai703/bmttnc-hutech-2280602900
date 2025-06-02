import tornado.ioloop
import tornado.web
import tornado.websocket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64 # Để gửi dữ liệu bytes qua WebSocket dưới dạng text

# Khóa AES và IV (Initialization Vector)
# Trong thực tế, khóa này nên được quản lý an toàn và có thể được tạo/trao đổi một cách bảo mật.
# Ví dụ này sử dụng một khóa cố định cho mục đích minh họa.
AES_KEY = get_random_bytes(16)  # Tạo một khóa AES 128-bit ngẫu nhiên khi server khởi động
                                # Để client giải mã được, khóa này cần được chia sẻ với client
                                # một cách an toàn, hoặc mỗi client có một session key riêng.
                                # Hiện tại, client sẽ không giải mã mà chỉ nhận chuỗi đã mã hóa.

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        print("Một client mới đã kết nối.")
        WebSocketServer.clients.add(self)

    def on_close(self):
        print("Một client đã ngắt kết nối.")
        WebSocketServer.clients.remove(self)

    def on_message(self, message_from_client: str):
        print(f"Server nhận được từ client: {message_from_client}")

        try:
            # Mã hóa thông điệp bằng AES
            cipher = AES.new(AES_KEY, AES.MODE_CBC) # Tạo cipher mới với IV mới mỗi lần
            message_bytes = message_from_client.encode('utf-8')
            padded_bytes = pad(message_bytes, AES.block_size)
            encrypted_bytes = cipher.encrypt(padded_bytes)

            # IV cần được gửi cùng với dữ liệu mã hóa để client (nếu cần giải mã) có thể sử dụng
            # Gửi IV + ciphertext dưới dạng base64 để dễ truyền qua WebSocket
            iv_b64 = base64.b64encode(cipher.iv).decode('utf-8')
            encrypted_data_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
            
            response_to_client = f"iv:{iv_b64};encrypted:{encrypted_data_b64}"
            
            print(f"Server gửi về client (đã mã hóa): {response_to_client}")
            self.write_message(response_to_client) # Gửi lại cho client đã gửi thông điệp

        except Exception as e:
            print(f"Lỗi khi mã hóa hoặc gửi tin nhắn: {e}")
            self.write_message(f"Lỗi phía server: {e}")

    # (Optional) Cần thiết cho một số trình duyệt hoặc proxy
    def check_origin(self, origin):
        return True

def main():
    app = tornado.web.Application(
        [(r"/websocket/", WebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)
    print("Server WebSocket đang lắng nghe trên cổng 8888...")
    print(f"Khóa AES được sử dụng (dạng hex): {AES_KEY.hex()}") # In khóa để biết (chỉ cho demo)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()