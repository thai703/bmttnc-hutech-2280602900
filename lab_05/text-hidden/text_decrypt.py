# text_encrypt.py
import sys

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text) + '00000000'  # Kết thúc bằng 8 số 0

def bin_to_zero_width(binary):
    return binary.replace('0', '\u200b').replace('1', '\u200c')

def encode_text(cover_text, message):
    binary_message = text_to_bin(message)
    zw_message = bin_to_zero_width(binary_message)
    return cover_text + zw_message

def main():
    if len(sys.argv) != 4:
        print("Usage: python text_encrypt.py <input_txt> <message> <output_txt>")
        return

    input_file = sys.argv[1]
    message = sys.argv[2]
    output_file = sys.argv[3]

    with open(input_file, "r", encoding="utf-8") as f:
        cover_text = f.read()

    stego_text = encode_text(cover_text, message)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(stego_text)

    print("✅ Mã hóa hoàn tất:", output_file)

if __name__ == "__main__":
    main()
