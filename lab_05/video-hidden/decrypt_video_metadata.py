import sys
from mutagen.mp4 import MP4

def decode_metadata(video_path):
    video = MP4(video_path)
    tags = video.tags
    if tags is not None and "\xa9cmt" in tags:
        print("🔓 Tin nhắn giải mã:", tags["\xa9cmt"][0])
    else:
        print("⚠️ Không tìm thấy message trong metadata.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decrypt_video_metadata.py <input_video>")
    else:
        decode_metadata(sys.argv[1])
