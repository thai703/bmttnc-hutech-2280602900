# ex05_cau02.py

import re

# Nhập chuỗi từ bàn phím (hoặc gán sẵn để test)
s = "-100#^sdfkj8902w3ir021@swf-20"

# Dùng regex để tìm tất cả các số nguyên (có thể có dấu - phía trước)
numbers = re.findall(r'-?\d+', s)

# Chuyển các chuỗi số thành số nguyên
numbers = [int(num) for num in numbers]

# Tính tổng
tong_duong = sum(num for num in numbers if num > 0)
tong_am = sum(num for num in numbers if num < 0)

# In kết quả
print("Chuỗi ban đầu là:", s)
print("Giá trị dương:", tong_duong)
print("Giá trị âm:", tong_am)
