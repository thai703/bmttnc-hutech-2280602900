import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- Triển khai MD5 Tùy chỉnh của Người dùng ---
# Sao chép chính xác các hàm từ script md5_hash.py của bạn

def left_rotate(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def custom_md5(message_as_bytes_input: bytes) -> str:
    """
    Tính toán mã băm MD5 bằng thuật toán tùy chỉnh được cung cấp.
    Input: message_as_bytes_input - chuỗi byte cần băm.
    Output: Chuỗi hex đại diện cho mã băm.
    """
    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    # --- Bắt đầu phần padding ---
    # Sử dụng bytearray để có thể thay đổi nội dung message cho việc padding
    message_for_padding = bytearray(message_as_bytes_input)
    
    # Lấy độ dài gốc của message (tính bằng byte) - theo logic script của bạn
    original_length_in_bytes = len(message_for_padding)

    # Thêm bit '1' (byte 0x80)
    message_for_padding.append(0x80)
    
    # Thêm các bit '0' (byte 0x00) cho đến khi độ dài message là 56 (mod 64)
    while len(message_for_padding) % 64 != 56:
        message_for_padding.append(0x00)
    
    # Thêm độ dài gốc (tính bằng byte, theo script của bạn) dưới dạng 64-bit little-endian
    message_for_padding.extend(original_length_in_bytes.to_bytes(8, 'little'))
    # --- Kết thúc phần padding ---

    # Chuyển lại thành bytes không thể thay đổi để xử lý các khối
    processed_message_bytes = bytes(message_for_padding)

    # Xử lý message theo từng khối 64-byte (512-bit)
    for i in range(0, len(processed_message_bytes), 64):
        block = processed_message_bytes[i:i+64]
        
        # Chia khối thành 16 từ 32-bit (little-endian)
        words = [int.from_bytes(block[j:j+4], 'little') for j in range(0, 64, 4)]
        
        # Khởi tạo các giá trị hash cho khối này
        a0, b0, c0, d0 = a, b, c, d
        
        # Vòng lặp chính (64 vòng) - theo logic script của bạn
        for j in range(64):
            f_val = 0
            g_val = 0
            if j < 16:
                f_val = (b & c) | ((~b) & d)
                g_val = j
            elif j < 32:
                f_val = (d & b) | ((~d) & c)
                g_val = (5*j + 1) % 16
            elif j < 48:
                f_val = b ^ c ^ d
                g_val = (3*j + 5) % 16
            else: # j < 64
                f_val = c ^ (b | (~d))
                g_val = (7*j) % 16
            
            temp = d
            d = c
            c = b
            # Sử dụng hằng số (0x5A827999) và phép quay (3) cố định từ script của bạn
            term_to_rotate = (a + f_val + 0x5A827999 + words[g_val]) & 0xFFFFFFFF
            rotated_term = left_rotate(term_to_rotate, 3)
            b = (b + rotated_term) & 0xFFFFFFFF
            a = temp

        # Cộng giá trị hash của khối này vào kết quả tính đến hiện tại
        a = (a + a0) & 0xFFFFFFFF
        b = (b + b0) & 0xFFFFFFFF
        c = (c + c0) & 0xFFFFFFFF
        d = (d + d0) & 0xFFFFFFFF
        
    # Tạo chuỗi hex kết quả cuối cùng
    return '{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d)

# --- Ứng dụng GUI ---
class CustomMD5GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom MD5 Hash Generator")
        self.geometry("650x530") # Kích thước cửa sổ (Rộng x Cao)

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
            bg="#28a745", fg="white", # Nút màu xanh lá
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
        
        # Ghi chú về việc đây là triển khai tùy chỉnh
        tk.Label(self, text="Lưu ý: Đây là UI cho mã MD5 tùy chỉnh được cung cấp, kết quả có thể khác với MD5 tiêu chuẩn.",
                 font=("Arial", 8, "italic"), fg="gray").pack(pady=(5,5), padx=10, anchor="w")


    def _display_in_scrolledtext(self, scrolled_text_widget: scrolledtext.ScrolledText, content: str):
        """Hiển thị nội dung trong một ScrolledText widget."""
        scrolled_text_widget.config(state=tk.NORMAL)
        scrolled_text_widget.delete('1.0', tk.END)
        scrolled_text_widget.insert(tk.END, content)
        scrolled_text_widget.config(state=tk.DISABLED)

    def gui_perform_hash(self):
        """Lấy dữ liệu đầu vào, tính toán hash bằng hàm custom_md5 và hiển thị kết quả."""
        input_string = self.input_text_area.get("1.0", tk.END).strip()

        if not input_string:
            messagebox.showwarning("Đầu vào trống", "Vui lòng nhập chuỗi văn bản để thực hiện băm.")
            self._display_in_scrolledtext(self.original_text_display, "")
            self._display_in_scrolledtext(self.hash_display_area, "")
            return

        try:
            # Mã hóa chuỗi đầu vào sang bytes (UTF-8 là phổ biến)
            message_bytes_to_hash = input_string.encode('utf-8')
            
            # Sử dụng hàm custom_md5 của bạn
            hashed_hex_string = custom_md5(message_bytes_to_hash) 

            # Hiển thị chuỗi văn bản gốc
            self._display_in_scrolledtext(self.original_text_display, input_string)
            
            # Hiển thị mã băm đã mã hóa hex
            self._display_in_scrolledtext(self.hash_display_area, hashed_hex_string)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi trong quá trình băm: {e}")
            self._display_in_scrolledtext(self.original_text_display, input_string) # Vẫn hiển thị input gốc
            self._display_in_scrolledtext(self.hash_display_area, f"Lỗi: {e}")

if __name__ == "__main__":
    app = CustomMD5GUI()
    app.mainloop()