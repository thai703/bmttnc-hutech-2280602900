import tkinter as tk
from tkinter import scrolledtext, messagebox
import hashlib # Sử dụng thư viện hashlib chuẩn của Python

# --- Hàm băm MD5 sử dụng hashlib (từ script của bạn) ---
def calculate_md5_from_library(input_string: str) -> str:
    """
    Tính toán mã băm MD5 của một chuỗi đầu vào bằng thư viện hashlib.
    Input: input_string - Chuỗi cần băm.
    Output: Chuỗi hex đại diện cho mã băm MD5.
    """
    md5_hash_object = hashlib.md5()
    md5_hash_object.update(input_string.encode('utf-8')) # Mã hóa sang bytes cho hashlib
    return md5_hash_object.hexdigest()

# --- Ứng dụng GUI ---
class MD5LibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MD5 Hash Generator (Thư viện hashlib)")
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
            text="Tính toán MD5 Hash",
            command=self.gui_perform_hash,
            font=("Arial", 12, "bold"),
            bg="#17a2b8", fg="white", # Nút màu xanh mòng két (teal)
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
        self.original_text_display.pack(fill="x", expand=False, pady=(0,15))

        tk.Label(output_frame, text="MD5 Hash:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0,5))
        self.hash_display_area = scrolledtext.ScrolledText(
            output_frame, height=6, wrap=tk.WORD, state=tk.DISABLED,
            font=("Courier New", 11, "bold"), bg="#e0e0e0", relief=tk.SOLID, borderwidth=1
        )
        self.hash_display_area.pack(fill="both", expand=True)

    def _display_in_scrolledtext(self, scrolled_text_widget: scrolledtext.ScrolledText, content: str):
        """Hiển thị nội dung trong một ScrolledText widget."""
        scrolled_text_widget.config(state=tk.NORMAL)
        scrolled_text_widget.delete('1.0', tk.END)
        scrolled_text_widget.insert(tk.END, content)
        scrolled_text_widget.config(state=tk.DISABLED)

    def gui_perform_hash(self):
        """Lấy dữ liệu đầu vào, tính toán hash bằng hàm calculate_md5_from_library và hiển thị kết quả."""
        input_string = self.input_text_area.get("1.0", tk.END).strip()

        if not input_string:
            messagebox.showwarning("Đầu vào trống", "Vui lòng nhập chuỗi văn bản để thực hiện băm.")
            self._display_in_scrolledtext(self.original_text_display, "")
            self._display_in_scrolledtext(self.hash_display_area, "")
            return

        try:
            # Sử dụng hàm calculate_md5_from_library (dùng hashlib.md5)
            hashed_hex_string = calculate_md5_from_library(input_string)

            # Hiển thị chuỗi văn bản gốc
            self._display_in_scrolledtext(self.original_text_display, input_string)
            
            # Hiển thị mã băm đã mã hóa hex
            self._display_in_scrolledtext(self.hash_display_area, hashed_hex_string)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi trong quá trình băm: {e}")
            self._display_in_scrolledtext(self.original_text_display, input_string) # Vẫn hiển thị input gốc
            self._display_in_scrolledtext(self.hash_display_area, f"Lỗi: {e}")

if __name__ == "__main__":
    app = MD5LibraryGUI()
    app.mainloop()