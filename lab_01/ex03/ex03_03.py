def tao_tuple_tu_list(lst):  # Đổi tên tham số từ 'list' (trùng keyword) thành 'lst'
    return tuple(lst)  # Đồng bộ tên tham số

# Nhập danh sách từ người dùng và xử lý chuỗi
input_list = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(int, input_list.split(',')))

# Chuyển đổi và in kết quả
my_tuple = tao_tuple_tu_list(numbers)
print("List:", numbers)  # Thêm dấu cách sau dấu phẩy cho đẹp
print("Tuple từ List:", my_tuple)