import tkinter as tk
from tkinter import messagebox
import base64

def encode_to_file():
    input_text = entry_input.get()
    if not input_text:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập chuỗi cần mã hóa.")
        return
    try:
        encoded = base64.b64encode(input_text.encode("utf-8")).decode("utf-8")
        with open("data.txt", "w") as file:
            file.write(encoded)
        messagebox.showinfo("Thành công", "Đã mã hóa và ghi vào tệp data.txt")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mã hóa: {e}")

def decode_from_file():
    try:
        with open("data.txt", "r") as file:
            encoded = file.read().strip()
        decoded = base64.b64decode(encoded).decode("utf-8")
        text_output.config(state="normal")
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, decoded)
        text_output.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể giải mã: {e}")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Mã hóa / Giải mã Base64")
root.geometry("400x300")

# Nhãn & ô nhập
tk.Label(root, text="Nhập chuỗi cần mã hóa:").pack(pady=5)
entry_input = tk.Entry(root, width=50)
entry_input.pack(pady=5)

# Nút mã hóa & giải mã
tk.Button(root, text="Mã hóa và ghi vào file", command=encode_to_file).pack(pady=5)
tk.Button(root, text="Giải mã từ file", command=decode_from_file).pack(pady=5)

# Hiển thị kết quả
tk.Label(root, text="Kết quả giải mã:").pack(pady=5)
text_output = tk.Text(root, height=5, width=50, state="disabled")
text_output.pack()

# Chạy ứng dụng
root.mainloop()
