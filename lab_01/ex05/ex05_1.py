import itertools

# Danh sách ban đầu
lst = [1, 2, 3]

# Lấy tất cả hoán vị
perms = list(itertools.permutations(lst))

# In ra kết quả
print("Tất cả hoán vị của danh sách", lst, "là:")
for p in perms:
    print(p)
