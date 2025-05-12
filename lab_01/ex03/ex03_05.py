def dem_so_lan_xuat_hien(lst):  # Sửa lại tên hàm (thiếu dấu '_' và dấu '(')
    count_dict = {}
    for item in lst:
        if item in count_dict:  # Thêm thụt lề
            count_dict[item] += 1  # Thêm thụt lề
        else:  # Thêm thụt lề
            count_dict[item] = 1  # Thêm thụt lề
    return count_dict

# Nhập danh sách từ người dùng
input_string = input("Nhập danh sách các từ, cách nhau bằng dấu cách: ")
word_list = input_string.split()

# Sử dụng hàm và in kết quả
so_lan_xuat_hien = dem_so_lan_xuat_hien(word_list)
print("Số lần xuất hiện của các phần tử:", so_lan_xuat_hien)  # Sửa "%6" thành "Số"