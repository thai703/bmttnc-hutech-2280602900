import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

output_path = "encoded_video.avi"
video_path = ""

# Hàm chuyển văn bản sang nhị phân
def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text) + '1111111111111110'  # dấu kết thúc

# Hàm chuyển nhị phân về văn bản
def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for c in chars:
        if c == '11111110':  # kết thúc
            break
        message += chr(int(c, 2))
    return message

# Mã hóa video
def encode_video(video_path, message, output_path="encoded_video.avi"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Lỗi", "Không thể mở video.")
        return

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    binary_message = text_to_bin(message)
    data_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if data_index < len(binary_message):
            for row in range(frame.shape[0]):
                for col in range(frame.shape[1]):
                    for channel in range(3):  # BGR
                        if data_index < len(binary_message):
                            frame[row][col][channel] = np.uint8(
                                (frame[row][col][channel] & 0b11111110) | int(binary_message[data_index])
                            )
                            data_index += 1
        out.write(frame)

    cap.release()
    out.release()
    messagebox.showinfo("Thành công", f"✅ Đã mã hóa và lưu video:\n{output_path}")

# Giải mã video
def decode_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Lỗi", "Không thể mở video.")
        return

    binary_data = ""
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for row in range(frame.shape[0]):
            for col in range(frame.shape[1]):
                for channel in range(3):  # BGR
                    binary_data += str(frame[row][col][channel] & 1)
                    if binary_data.endswith('11111110'):
                        cap.release()
                        message = bin_to_text(binary_data)
                        messagebox.showinfo("🔓 Tin nhắn đã giải mã", message)
                        return
    cap.release()
    messagebox.showwarning("⚠️ Không tìm thấy thông điệp", "Không tìm thấy kết thúc hợp lệ.")

# Giao diện UI
def select_video_encode():
    global video_path
    video_path = filedialog.askopenfilename(title="Chọn video để mã hóa", filetypes=[("Video files", "*.avi *.mp4")])
    label_video_path.config(text=f"Video đã chọn: {video_path}")

def select_output_path():
    global output_path
    output_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
    label_output_path.config(text=f"Lưu thành: {output_path}")

def run_encode():
    if not video_path or not message_entry.get():
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn video và nhập tin nhắn.")
        return
    encode_video(video_path, message_entry.get(), output_path)

def run_decode():
    video_to_decode = filedialog.askopenfilename(title="Chọn video để giải mã", filetypes=[("Video files", "*.avi *.mp4")])
    if video_to_decode:
        decode_video(video_to_decode)

# UI chính
root = tk.Tk()
root.title("📦 Video Steganography")
root.geometry("500x350")
root.resizable(False, False)

tk.Label(root, text="📼 Giấu tin nhắn vào video", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="🗂 Chọn video", command=select_video_encode).pack()
label_video_path = tk.Label(root, text="Video đã chọn: (chưa chọn)", fg="blue")
label_video_path.pack()

tk.Label(root, text="💬 Nhập tin nhắn cần giấu:").pack(pady=5)
message_entry = tk.Entry(root, width=50)
message_entry.pack()

tk.Button(root, text="💾 Chọn nơi lưu video", command=select_output_path).pack(pady=5)
label_output_path = tk.Label(root, text="Lưu thành: encoded_video.avi (mặc định)", fg="green")
label_output_path.pack()

tk.Button(root, text="🚀 Mã hóa", bg="lightgreen", command=run_encode).pack(pady=10)

tk.Label(root, text="-----------------------").pack(pady=5)

tk.Button(root, text="🔍 Giải mã từ video", bg="lightblue", command=run_decode).pack(pady=5)

root.mainloop()
