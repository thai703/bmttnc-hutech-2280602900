# text_hidden_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text) + '00000000'

def bin_to_zero_width(binary):
    return binary.replace('0', '\u200b').replace('1', '\u200c')

def zero_width_to_bin(zw_text):
    return zw_text.replace('\u200b', '0').replace('\u200c', '1')

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for c in chars:
        if c == '00000000':
            break
        message += chr(int(c, 2))
    return message

def encode_text(cover_text, message):
    binary_message = text_to_bin(message)
    zw_message = bin_to_zero_width(binary_message)
    return cover_text + zw_message

def decode_text(stego_text):
    zw_chars = ''.join(c for c in stego_text if c in ['\u200b', '\u200c'])
    binary_data = zero_width_to_bin(zw_chars)
    return bin_to_text(binary_data)

# ==== GUI ====
def select_file():
    global input_file
    input_file = filedialog.askopenfilename(title="Chọn file văn bản", filetypes=[("Text files", "*.txt")])
    lbl_file.config(text=f"File: {input_file}")

def save_file(content):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Thành công", f"Đã lưu: {save_path}")

def run_encode():
    if not input_file or not entry_message.get():
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn file và nhập tin nhắn.")
        return
    with open(input_file, "r", encoding="utf-8") as f:
        cover_text = f.read()

    stego_text = encode_text(cover_text, entry_message.get())
    save_file(stego_text)

def run_decode():
    decode_file = filedialog.askopenfilename(title="Chọn file đã mã hóa", filetypes=[("Text files", "*.txt")])
    if decode_file:
        with open(decode_file, "r", encoding="utf-8") as f:
            stego_text = f.read()
        message = decode_text(stego_text)
        messagebox.showinfo("Tin nhắn đã giải mã", message)

# ==== UI ====
root = tk.Tk()
root.title("📜 Giấu tin trong văn bản")
root.geometry("500x300")
root.resizable(False, False)

tk.Label(root, text="📜 Giấu tin nhắn trong văn bản", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="🗂 Chọn file văn bản", command=select_file).pack()
lbl_file = tk.Label(root, text="File: (chưa chọn)", fg="blue")
lbl_file.pack()

tk.Label(root, text="💬 Nhập tin nhắn cần giấu:").pack(pady=5)
entry_message = tk.Entry(root, width=50)
entry_message.pack()

tk.Button(root, text="🚀 Mã hóa và lưu", bg="lightgreen", command=run_encode).pack(pady=10)

tk.Label(root, text="-----------------------").pack(pady=5)

tk.Button(root, text="🔍 Giải mã từ file", bg="lightblue", command=run_decode).pack(pady=5)

root.mainloop()
