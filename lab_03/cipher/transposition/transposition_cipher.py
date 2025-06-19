class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        num_rows = (len(text) + key - 1) // key
        num_full_columns = len(text) % key
        if num_full_columns == 0:
            num_full_columns = key

        # Tính chiều dài từng cột
        col_lengths = [num_rows] * num_full_columns + [num_rows - 1] * (key - num_full_columns)

        # Chia text thành các cột
        index = 0
        columns = []
        for length in col_lengths:
            columns.append(text[index:index + length])
            index += length

        # Đọc theo hàng (zigzag)
        result = ''
        for row in range(num_rows):
            for col in range(key):
                if row < len(columns[col]):
                    result += columns[col][row]
        return result
