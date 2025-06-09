import cv2
def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for c in chars:
        if c == '11111110':  # kết thúc
            break
        message += chr(int(c, 2))
    return message

def decode_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Không thể mở video.")
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
                        print("🔓 Tin nhắn giải mã:", bin_to_text(binary_data))
                        return
    cap.release()
    print("⚠️ Không tìm thấy thông điệp kết thúc hợp lệ.")
