import wave
import tkinter as tk
from tkinter import filedialog, messagebox

# === Encode ===
def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text) + '00000000'

def encode_audio(input_audio, message, output_audio):
    audio = wave.open(input_audio, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    binary_message = text_to_bin(message)
    data_index = 0

    for i in range(len(frame_bytes)):
        if data_index < len(binary_message):
            frame_bytes[i] = (frame_bytes[i] & 254) | int(binary_message[data_index])
            data_index += 1

    encoded_audio = wave.open(output_audio, 'wb')
    encoded_audio.setparams(audio.getparams())
    encoded_audio.writeframes(bytes(frame_bytes))

    audio.close()
    encoded_audio.close()

    messagebox.showinfo("✅ Thành công", f"Audio đã mã hóa: {output_audio}")

# === Decode ===
def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for c in chars:
        if c == '00000000':
            break
        message += chr(int(c, 2))
    return message

def decode_audio(stego_audio):
    audio = wave.open(stego_audio, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    extracted_bits = [str(frame_bytes[i] & 1) for i in range(len(frame_bytes))]
    binary_message = ''.join(extracted_bits)
    message = bin_to_text(binary_message)

    audio.close()
    messagebox.showinfo("🔓 Tin nhắn giải mã", message)

# === UI ===
def select_input_audio():
    global input_audio_path
    input_audio_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    lbl_input_audio.config(text=f"Đã chọn: {input_audio_path}")

def select_output_audio():
    global output_audio_path
    output_audio_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    lbl_output_audio.config(text=f"Lưu thành: {output_audio_path}")

def run_encode():
    if not input_audio_path or not entry_message.get():
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn audio và nhập tin nhắn.")
        return
    encode_audio(input_audio_path, entry_message.get(), output_audio_path)

def run_decode():
    audio_to_decode = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if audio_to_decode:
        decode_audio(audio_to_decode)

# === MAIN ===
root = tk.Tk()
root.title("🎵 Audio Steganography")
root.geometry("500x350")
root.resizable(False, False)

input_audio_path = ""
output_audio_path = "stego_audio.wav"

tk.Label(root, text="🎵 Giấu tin nhắn vào Audio (WAV)", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="🗂 Chọn audio đầu vào", command=select_input_audio).pack()
lbl_input_audio = tk.Label(root, text="(Chưa chọn file)", fg="blue")
lbl_input_audio.pack()

tk.Label(root, text="💬 Nhập tin nhắn cần giấu:").pack(pady=5)
entry_message = tk.Entry(root, width=50)
entry_message.pack()

tk.Button(root, text="💾 Chọn nơi lưu", command=select_output_audio).pack(pady=5)
lbl_output_audio = tk.Label(root, text="Lưu thành: stego_audio.wav (mặc định)", fg="green")
lbl_output_audio.pack()

tk.Button(root, text="🚀 Mã hóa", bg="lightgreen", command=run_encode).pack(pady=10)

tk.Label(root, text="-----------------------").pack(pady=5)

tk.Button(root, text="🔍 Giải mã từ audio", bg="lightblue", command=run_decode).pack(pady=5)

root.mainloop()
