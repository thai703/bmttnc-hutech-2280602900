import sys
import ffmpeg
from mutagen.mp4 import MP4, MP4Tags

def encode_metadata(input_video, message, output_video):
    # Copy video vào file mới
    ffmpeg.input(input_video).output(output_video, c='copy').run(overwrite_output=True)
    
    # Ghi message vào metadata
    video = MP4(output_video)
    if video.tags is None:
        video.add_tags()
    
    video.tags["\xa9cmt"] = message  # Tag comment
    video.save()
    
    print(f"✅ Đã mã hóa và lưu video: {output_video}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python encrypt_video_metadata.py <input_video> <message> <output_video>")
    else:
        encode_metadata(sys.argv[1], sys.argv[2], sys.argv[3])
