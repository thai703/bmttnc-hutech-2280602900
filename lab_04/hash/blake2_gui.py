import tkinter as tk
from tkinter import scrolledtext, messagebox
import hashlib

# --- Hàm băm BLAKE2b (từ script của bạn) ---
def calculate_blake2b_hash(message_bytes: bytes) -> bytes:
    """
    Tính toán mã băm BLAKE2b cho một chuỗi bytes.
    Sử dụng digest_size=64 để có kết quả 64 byte (512-bit).
    """
    blake2_hash_obj = hashlib.blake2b(digest_size=64)
    blake2_hash_obj.update(message_bytes)
    return blake2_hash_obj.digest() # Trả về dưới dạng bytes

# --- Ứng dụng GUI ---
class Blake2GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BLAKE2b Hash Generator")
        self.geometry("650x500") # Kích thước cửa sổ (Rộng x Cao)

        self.init_ui()

    def init_ui(self):
        # --- Khung Nhập liệu ---
        input_frame = tk.LabelFrame(self, text="Đầu vào", padx=15, pady=15, font=("Arial", 11))
        input_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(input_frame, text="Nhập chuỗi văn bản cần băm:", font=("Arial", 10)).pack(anchor="w", pady=(0,5))
        self.input_text_area = scrolledtext.ScrolledText(input_frame, height=6, wrap=tk.WORD, font=("Arial", 10), relief=tk.SOLID, borderwidth=1)
        self.input_text_area.pack(fill="x", expand=True, pady=(0,10))
        self.input_text_area.focus() # Đặt con trỏ vào ô nhập liệu khi mở

        btn_calculate = tk.Button(
            input_frame,
            text="Tính toán BLAKE2",
            command=self.gui_perform_hash,
            font=("Arial", 12, "bold"),
            bg="#007bff", fg="white",
            relief=tk.RAISED, borderwidth=2,
            padx=10, pady=5
        )
        btn_calculate.pack(pady=5, fill="x")

        # --- Khung Kết quả ---
        output_frame = tk.LabelFrame(self, text="Kết quả", padx=15, pady=15, font=("Arial", 11))
        output_frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(output_frame, text="Chuỗi văn bản đã nhập:", font=("Arial", 10)).pack(anchor="w", pady=(0,5))
        self.original_text_display = scrolledtext.ScrolledText(
            output_frame, height=4, wrap=tk.WORD, state=tk.DISABLED,
            font=("Arial", 10), bg="#f0f0f0", relief=tk.SOLID, borderwidth=1
        )
        self.original_text_display.pack(fill="x", expand=False, pady=(0,15)) # expand=False để không chiếm quá nhiều không gian

        tk.Label(output_frame, text="BLAKE2 Hash:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0,5))
        self.hash_display_area = scrolledtext.ScrolledText(
            output_frame, height=6, wrap=tk.WORD, state=tk.DISABLED,
            font=("Courier New", 11, "bold"), bg="#e0e0e0", relief=tk.SOLID, borderwidth=1 # Font Courier New để dễ đọc mã hex
        )
        self.hash_display_area.pack(fill="both", expand=True)

    def _display_in_scrolledtext(self, scrolled_text_widget: scrolledtext.ScrolledText, content: str):
        """Hiển thị nội dung trong một ScrolledText widget (cho phép chỉnh sửa tạm thời để cập nhật)."""
        scrolled_text_widget.config(state=tk.NORMAL)
        scrolled_text_widget.delete('1.0', tk.END)
        scrolled_text_widget.insert(tk.END, content)
        scrolled_text_widget.config(state=tk.DISABLED)

    def gui_perform_hash(self):
        """Lấy dữ liệu đầu vào, tính toán hash và hiển thị kết quả."""
        input_string = self.input_text_area.get("1.0", tk.END).strip() # Lấy toàn bộ text và loại bỏ khoảng trắng thừa

        if not input_string:
            messagebox.showwarning("Đầu vào trống", "Vui lòng nhập chuỗi văn bản để thực hiện băm.")
            self._display_in_scrolledtext(self.original_text_display, "")
            self._display_in_scrolledtext(self.hash_display_area, "")
            return

        try:
            # Mã hóa chuỗi đầu vào sang bytes (UTF-8 là phổ biến)
            message_bytes = input_string.encode('utf-8')

            # Tính toán mã băm BLAKE2b
            hashed_bytes = calculate_blake2b_hash(message_bytes)
            hashed_hex_string = hashed_bytes.hex() # Chuyển sang dạng hex string

            # Hiển thị chuỗi văn bản gốc
            self._display_in_scrolledtext(self.original_text_display, input_string)
            
            # Hiển thị mã băm đã mã hóa hex
            self._display_in_scrolledtext(self.hash_display_area, hashed_hex_string)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi trong quá trình băm: {e}")
            self._display_in_scrolledtext(self.original_text_display, input_string) # Vẫn hiển thị input gốc
            self._display_in_scrolledtext(self.hash_display_area, f"Lỗi: {e}")


if __name__ == "__main__":
    app = Blake2GUI()
    app.mainloop()