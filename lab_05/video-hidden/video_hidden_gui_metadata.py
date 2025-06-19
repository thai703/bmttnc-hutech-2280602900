import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg
from mutagen.mp4 import MP4

# Ghi metadata
def encode_metadata(input_video, message, output_video):
    ffmpeg.input(input_video).output(output_video, c='copy').run(overwrite_output=True)
    video = MP4(output_video)
    if video.tags is None:
        video.add_tags()
    video.tags["\xa9cmt"] = message
    video.save()
    return output_video

# Đọc metadata
def decode_metadata(video_path):
    video = MP4(video_path)
    tags = video.tags
    if tags is not None and "\xa9cmt" in tags:
        return tags["\xa9cmt"][0]
    else:
        return None

# GUI
class VideoHiddenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Video Steganography (Metadata)")
        self.root.geometry("500x350")

        # Input
        self.video_path = ""
        self.output_path = ""

        tk.Button(root, text="📂 Chọn video", command=self.select_video).pack(pady=10)
        self.label_video = tk.Label(root, text="Chưa chọn video", fg="blue")
        self.label_video.pack()

        tk.Label(root, text="💬 Nhập tin nhắn cần giấu:").pack(pady=5)
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack()

        tk.Button(root, text="💾 Chọn nơi lưu video", command=self.select_output).pack(pady=5)
        self.label_output = tk.Label(root, text="Lưu thành: (chưa chọn)", fg="green")
        self.label_output.pack()

        tk.Button(root, text="🚀 Mã hóa", bg="lightgreen", command=self.run_encode).pack(pady=10)

        tk.Label(root, text="------------------------").pack(pady=5)

        tk.Button(root, text="🔍 Giải mã từ video", bg="lightblue", command=self.run_decode).pack(pady=5)

    def select_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")])
        if path:
            self.video_path = path
            self.label_video.config(text=f"Đã chọn: {path}")

    def select_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if path:
            self.output_path = path
            self.label_output.config(text=f"Lưu thành: {path}")

    def run_encode(self):
        if not self.video_path or not self.output_path or not self.message_entry.get():
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn video, nhập message và chọn nơi lưu.")
            return
        encode_metadata(self.video_path, self.message_entry.get(), self.output_path)
        messagebox.showinfo("✅ Thành công", f"Video đã mã hóa: {self.output_path}")

    def run_decode(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")])
        if path:
            message = decode_metadata(path)
            if message:
                messagebox.showinfo("🔓 Tin nhắn đã giải mã", message)
            else:
                messagebox.showwarning("⚠️ Không tìm thấy message", "Không có message trong metadata.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoHiddenApp(root)
    root.mainloop()
