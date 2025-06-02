import tornado.ioloop
import tornado.websocket
import threading
# import base64 # Nếu client cần giải mã thì sẽ dùng đến
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad

# Biến toàn cục để lưu đối tượng kết nối WebSocket
ws_connection = None

# Khóa AES (nếu client cần giải mã, phải giống khóa trên server và được truyền an toàn)
# AES_KEY_CLIENT = bytes.fromhex("HEX_CUA_AES_KEY_TU_SERVER") # Ví dụ

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop
        self.url = "ws://localhost:8888/websocket/"

    async def connect(self):
        print(f"Đang cố gắng kết nối đến {self.url}")
        try:
            self.connection = await tornado.websocket.websocket_connect(
                self.url,
                on_message_callback=self.on_message,
                ping_interval=10,
                ping_timeout=30
            )
            global ws_connection
            ws_connection = self.connection # Lưu kết nối
            print("Đã kết nối thành công đến server!")
        except Exception as e:
            print(f"Kết nối thất bại: {e}")
            # Có thể thêm logic thử kết nối lại ở đây nếu muốn
            self.io_loop.stop()


    def on_message(self, message_from_server):
        if message_from_server is None:
            print("Ngắt kết nối từ server. Đang thử kết nối lại...")
            global ws_connection
            ws_connection = None # Xóa kết nối cũ
            # Có thể gọi lại self.connect() hoặc một hàm xử lý kết nối lại
            # Tuy nhiên, tornado.websocket.websocket_connect không nên gọi lại trực tiếp từ on_message
            # khi message is None mà không có cơ chế quản lý cẩn thận.
            # Thay vào đó, luồng chính có thể quản lý việc này.
            # Hiện tại, chúng ta sẽ dừng io_loop và yêu cầu người dùng chạy lại client.
            print("Vui lòng chạy lại client để kết nối lại.")
            self.io_loop.stop()

            return

        print(f"Client nhận được từ server (đã mã hóa): {message_from_server}")
        
        # --- Phần giải mã (Nếu client cần giải mã) ---
        # try:
        #     # Tách IV và dữ liệu mã hóa
        #     parts = message_from_server.split(';')
        #     iv_b64 = parts[0].split(':')[1]
        #     encrypted_data_b64 = parts[1].split(':')[1]
            
        #     iv = base64.b64decode(iv_b64)
        #     encrypted_bytes = base64.b64decode(encrypted_data_b64)
            
        #     cipher_decrypt = AES.new(AES_KEY_CLIENT, AES.MODE_CBC, iv)
        #     decrypted_padded_bytes = cipher_decrypt.decrypt(encrypted_bytes)
        #     decrypted_original_bytes = unpad(decrypted_padded_bytes, AES.block_size)
        #     decrypted_message = decrypted_original_bytes.decode('utf-8')
            
        #     print(f"Client đã giải mã: {decrypted_message}")
        # except Exception as e:
        #     print(f"Lỗi khi giải mã: {e}. Dữ liệu gốc từ server: {message_from_server}")
        # --- Kết thúc phần giải mã ---


    def send_message(self, message_to_send: str):
        if self.connection:
            print(f"Client gửi đến server: {message_to_send}")
            self.connection.write_message(message_to_send)
        else:
            print("Chưa kết nối đến server. Không thể gửi tin nhắn.")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Đã đóng kết nối.")


def listen_for_input(client_instance: WebSocketClient):
    """Hàm chạy trong một luồng riêng để nhận input từ người dùng."""
    while True:
        try:
            message = input("Nhập thông điệp gửi đến server (gõ 'exit' để thoát): \n> ")
            if message.lower() == 'exit':
                client_instance.close_connection()
                # Dừng IOLoop một cách an toàn từ luồng khác
                client_instance.io_loop.add_callback(client_instance.io_loop.stop)
                break
            if ws_connection: # Kiểm tra xem kết nối còn tồn tại không
                 # Gửi tin nhắn từ luồng chính của IOLoop để đảm bảo thread-safety với Tornado
                client_instance.io_loop.add_callback(client_instance.send_message, message)
            else:
                print("Mất kết nối tới server. Không thể gửi tin nhắn. Vui lòng khởi động lại client.")
                # Dừng IOLoop nếu mất kết nối
                client_instance.io_loop.add_callback(client_instance.io_loop.stop)
                break
        except KeyboardInterrupt: # Xử lý Ctrl+C
            print("\nĐang thoát client...")
            client_instance.close_connection()
            client_instance.io_loop.add_callback(client_instance.io_loop.stop)
            break
        except Exception as e:
            print(f"Lỗi khi nhận input hoặc gửi tin: {e}")
            client_instance.close_connection()
            client_instance.io_loop.add_callback(client_instance.io_loop.stop)
            break


async def main_async():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    
    # Chạy hàm connect bất đồng bộ
    await client.connect() 
    
    # Nếu kết nối thành công, bắt đầu luồng nhận input
    if client.connection:
        input_thread = threading.Thread(target=listen_for_input, args=(client,), daemon=True)
        input_thread.start()
    else:
        print("Không thể bắt đầu luồng nhập liệu do kết nối ban đầu thất bại.")
        # io_loop đã được stop trong hàm connect nếu lỗi

if __name__ == "__main__":
    # Sử dụng tornado.ioloop.IOLoop.run_sync cho hàm main bất đồng bộ
    # hoặc quản lý IOLoop như dưới đây nếu có các tác vụ khác cần chạy trước/sau khi start IOLoop
    
    io_loop_instance = tornado.ioloop.IOLoop.current()
    io_loop_instance.add_callback(main_async) # Thêm main_async vào callback của IOLoop
    try:
        io_loop_instance.start()
    except KeyboardInterrupt:
        print("Client bị dừng bởi người dùng.")
    finally:
        if ws_connection:
            ws_connection.close()
        print("Client đã thoát.")