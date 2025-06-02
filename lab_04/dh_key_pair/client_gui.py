import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
# cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # Không dùng trong GUI này
# from cryptography.hazmat.primitives import hashes # Không dùng trong GUI này

# --- Các hàm Diffie-Hellman cần thiết cho Client ---
def generate_client_key_pair_func(parameters):
    """Tạo cặp khóa DH cho client từ tham số đã cho."""
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_secret_func(client_private_key, server_public_key):
    """Tính toán shared secret."""
    shared_key_bytes = client_private_key.exchange(server_public_key)
    return shared_key_bytes

# --- Ứng dụng GUI cho Client ---
class DHClientGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DH Client - Derive Shared Secret")
        self.geometry("600x450")

        # Biến trạng thái nội bộ
        self.loaded_server_public_key_obj = None
        self.client_private_key = None
        # self.client_public_key_obj = None # Không cần hiển thị public key của client
        self.shared_secret_bytes = None
        self.server_public_key_pem_path = "" # Sẽ được người dùng chọn

        self.init_ui()

    def init_ui(self):
        # --- Khung điều khiển ---
        control_frame = tk.Frame(self, padx=10, pady=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(control_frame, text="Đường dẫn file Public Key Server:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0,5))
        self.server_pubkey_path_entry = tk.Entry(control_frame, width=40, font=("Arial", 10))
        self.server_pubkey_path_entry.pack(side=tk.LEFT, padx=5, ipady=3, expand=True, fill=tk.X)
        
        btn_browse_load = tk.Button(control_frame, text="Chọn File...", command=self.gui_browse_load_server_pubkey_path, font=("Arial", 10))
        btn_browse_load.pack(side=tk.LEFT, padx=5)

        # Nút để load public key server và tính toán shared secret
        btn_derive_secret = tk.Button(self, text="Load Public Key Server & Tính Shared Secret",
                                      command=self.gui_load_and_derive_secret,
                                      font=("Arial", 12, "bold"), height=2, bg="#007bff", fg="white")
        btn_derive_secret.pack(pady=20, padx=20, fill=tk.X)

        # --- Khu vực hiển thị Shared Secret ---
        tk.Label(self, text="Shared Secret:", font=("Arial", 11, "bold")).pack(pady=(10,0))
        self.shared_secret_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10, font=("Courier New", 10), relief=tk.SUNKEN, borderwidth=1)
        self.shared_secret_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.shared_secret_area.config(state=tk.DISABLED)

        # --- Log messages (tùy chọn, có thể bỏ nếu chỉ muốn hiện shared secret) ---
        # tk.Label(self, text="Log:", font=("Arial", 9)).pack(pady=(5,0))
        # self.log_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=5, font=("Arial", 8))
        # self.log_area.pack(padx=20, pady=5, fill=tk.X, expand=False)
        # self.log_area.config(state=tk.DISABLED)


    def _log(self, message, area="log"): # Thêm tham số area để chọn nơi log
        """Ghi log ra khu vực được chọn."""
        target_area = self.shared_secret_area # Mặc định là shared_secret_area nếu log_area bị ẩn
        # if area == "log" and hasattr(self, 'log_area'): # Kiểm tra nếu log_area tồn tại
        #     target_area = self.log_area
        
        target_area.config(state=tk.NORMAL)
        if area == "secret": # Nếu là secret thì xóa nội dung cũ
            target_area.delete('1.0', tk.END)
            target_area.insert(tk.END, message + "\n")
        # elif hasattr(self, 'log_area'): # Chỉ log thường nếu log_area hiển thị
        #     target_area.insert(tk.END, message + "\n")
        target_area.config(state=tk.DISABLED)
        target_area.yview(tk.END)


    def gui_browse_load_server_pubkey_path(self):
        """Mở dialog để chọn file public key của server để load."""
        path = filedialog.askopenfilename(defaultextension=".pem",
                                             filetypes=[("PEM files", "*.pem"), ("All files", "*.*")],
                                             title="Chọn file Public Key của Server")
        if path:
            self.server_public_key_pem_path = path
            self.server_pubkey_path_entry.delete(0, tk.END)
            self.server_pubkey_path_entry.insert(0, self.server_public_key_pem_path)
            # self._log(f"Đã chọn file public key server: {self.server_public_key_pem_path}", area="log")

    def gui_load_and_derive_secret(self):
        """Load public key server, tạo khóa client, và tính shared secret."""
        self.server_public_key_pem_path = self.server_pubkey_path_entry.get()
        if not self.server_public_key_pem_path.strip():
            messagebox.showerror("Lỗi", "Vui lòng chọn file Public Key của Server.")
            # self._log("Lỗi: Đường dẫn file public key server trống.", area="log")
            return

        try:
            # 1. Load Public Key của Server
            with open(self.server_public_key_pem_path, "rb") as f:
                self.loaded_server_public_key_obj = serialization.load_pem_public_key(f.read())
            # self._log(f"Đã load public key server từ: {self.server_public_key_pem_path}", area="log")

            if not isinstance(self.loaded_server_public_key_obj, dh.DHPublicKey):
                messagebox.showerror("Lỗi File", "File đã chọn không phải là DH Public Key hợp lệ.")
                # self._log("Lỗi: File không phải DH Public Key.", area="log")
                return

            # 2. Tạo cặp khóa Client
            client_params = self.loaded_server_public_key_obj.parameters()
            self.client_private_key, _ = generate_client_key_pair_func(client_params) # Public key của client không cần lưu trữ
            # self._log("Đã tạo cặp khóa cho client.", area="log")

            # 3. Tính toán Shared Secret
            self.shared_secret_bytes = derive_shared_secret_func(self.client_private_key, self.loaded_server_public_key_obj)
            # self._log("Đã tính toán Shared Secret thành công!", area="log")
            
            # Hiển thị Shared Secret
            self._log(f"{self.shared_secret_bytes.hex()}", area="secret")
            messagebox.showinfo("Thành công", "Đã tính toán và hiển thị Shared Secret!")

        except FileNotFoundError:
            # self._log(f"Lỗi: Không tìm thấy file public key server tại {self.server_public_key_pem_path}", area="log")
            messagebox.showerror("Lỗi File", f"Không tìm thấy file: {self.server_public_key_pem_path}")
            self.shared_secret_area.config(state=tk.NORMAL)
            self.shared_secret_area.delete('1.0', tk.END) # Xóa nếu có lỗi
            self.shared_secret_area.config(state=tk.DISABLED)
        except Exception as e:
            # self._log(f"Lỗi trong quá trình xử lý: {e}", area="log")
            messagebox.showerror("Lỗi Xử Lý", f"Đã xảy ra lỗi: {e}")
            self.shared_secret_area.config(state=tk.NORMAL)
            self.shared_secret_area.delete('1.0', tk.END) # Xóa nếu có lỗi
            self.shared_secret_area.config(state=tk.DISABLED)


if __name__ == "__main__":
    # Giả định file server_public_key.pem đã tồn tại
    # Bạn cần chạy server.py (script gốc của bạn) một lần để tạo file này trước.
    app = DHClientGUI()
    app.mainloop()