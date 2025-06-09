import cv2
import numpy as np

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text) + '1111111111111110'  # dấu kết thúc

def encode_video(video_path, message, output_path="encoded_video.avi"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Không thể mở video.")
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
                            frame[row][col][channel] = (frame[row][col][channel] & ~1) | int(binary_message[data_index])
                            data_index += 1
        out.write(frame)

    cap.release()
    out.release()
    print("✅ Đã mã hóa và lưu video thành công:", output_path)
