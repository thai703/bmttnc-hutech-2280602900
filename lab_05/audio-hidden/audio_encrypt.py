import wave
import sys

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

    print("✅ Audio đã mã hóa:", output_audio)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python audio_encrypt.py <input_audio.wav> <message> <output_audio.wav>")
    else:
        encode_audio(sys.argv[1], sys.argv[2], sys.argv[3])
