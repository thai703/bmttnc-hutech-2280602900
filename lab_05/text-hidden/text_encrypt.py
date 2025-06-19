# text_decrypt.py
import sys

def zero_width_to_bin(zw_text):
    return zw_text.replace('\u200b', '0').replace('\u200c', '1')

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for c in chars:
        if c == '00000000':
            break
        message += chr(int(c, 2))
    return message

def decode_text(stego_text):
    zw_chars = ''.join(c for c in stego_text if c in ['\u200b', '\u200c'])
    binary_data = zero_width_to_bin(zw_chars)
    return bin_to_text(binary_data)

def main():
    if len(sys.argv) != 2:
        print("Usage: python text_decrypt.py <stego_txt>")
        return

    input_file = sys.argv[1]

    with open(input_file, "r", encoding="utf-8") as f:
        stego_text = f.read()

    message = decode_text(stego_text)
    print("🔓 Tin nhắn giải mã:", message)

if __name__ == "__main__":
    main()
