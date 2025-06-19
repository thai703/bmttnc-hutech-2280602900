import wave
import sys

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

    print("🔓 Tin nhắn giải mã:", message)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python audio_decrypt.py <stego_audio.wav>")
    else:
        decode_audio(sys.argv[1])
