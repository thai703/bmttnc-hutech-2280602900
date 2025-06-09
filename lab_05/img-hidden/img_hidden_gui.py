import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# ================= Encoding Function =================
def encode_image(image_path, message):
    try:
        img = Image.open(image_path)
        width, height = img.size

        message += "####END####"
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        data_index = 0

        for row in range(height):
            for col in range(width):
                pixel = list(img.getpixel((col, row)))
                for color_channel in range(3):
                    if data_index < len(binary_message):
                        pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                        data_index += 1
                img.putpixel((col, row), tuple(pixel))
                if data_index >= len(binary_message):
                    break
            if data_index >= len(binary_message):
                break

        save_path = os.path.join(os.path.dirname(image_path), "encoded_image.png")
        img.save(save_path)
        return save_path
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mã hóa hình ảnh: {e}")
        return None

# ================= Decoding Function =================
def decode_image(encoded_image_path):
    try:
        img = Image.open(encoded_image_path)
        width, height = img.size
        binary_message = ""

        for row in range(height):
            for col in range(width):
                pixel = img.getpixel((col, row))
                for color_channel in range(3):
                    binary_message += format(pixel[color_channel], '08b')[-1]

        message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            char = chr(int(byte, 2))
            message += char
            if message.endswith("####END####"):
                break

        return message.replace("####END####", "")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể giải mã hình ảnh: {e}")
        return None

# ================= UI =================
class ImgHiddenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")

        self.label = tk.Label(root, text="Chọn hình ảnh và nhập thông điệp:")
        self.label.pack(pady=10)

        self.btn_browse = tk.Button(root, text="Chọn ảnh", command=self.browse_image)
        self.btn_browse.pack(pady=5)

        self.image_path = ""
        self.message_entry = tk.Entry(root, width=60)
        self.message_entry.pack(pady=5)

        self.btn_encode = tk.Button(root, text="Mã hóa thông điệp vào ảnh", command=self.encode)
        self.btn_encode.pack(pady=10)

        self.btn_decode = tk.Button(root, text="Giải mã ảnh đã mã hóa", command=self.decode)
        self.btn_decode.pack(pady=10)

        self.output = tk.Text(root, height=8, width=70)
        self.output.pack(pady=10)

    def browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if path:
            self.image_path = path
            self.label.config(text=f"Đã chọn ảnh: {os.path.basename(path)}")

    def encode(self):
        if not self.image_path:
            messagebox.showwarning("Chưa chọn ảnh", "Vui lòng chọn một ảnh để mã hóa.")
            return
        message = self.message_entry.get()
        if not message:
            messagebox.showwarning("Chưa có thông điệp", "Vui lòng nhập thông điệp để mã hóa.")
            return
        save_path = encode_image(self.image_path, message)
        if save_path:
            messagebox.showinfo("Thành công", f"Ảnh đã mã hóa được lưu tại: {save_path}")

    def decode(self):
        path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if path:
            decoded = decode_image(path)
            if decoded is not None:
                self.output.delete(1.0, tk.END)
                self.output.insert(tk.END, f"Thông điệp đã giải mã: {decoded}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ImgHiddenApp(root)
    root.mainloop()
