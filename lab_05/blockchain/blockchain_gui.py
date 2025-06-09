import tkinter as tk
from tkinter import messagebox, scrolledtext
from blockchain import Blockchain

# Khởi tạo blockchain
my_blockchain = Blockchain()

def add_transaction():
    sender = entry_sender.get()
    receiver = entry_receiver.get()
    amount = entry_amount.get()

    if not sender or not receiver or not amount:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng điền đầy đủ thông tin giao dịch.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Lỗi", "Số tiền không hợp lệ.")
        return

    index = my_blockchain.add_transaction(sender, receiver, amount)
    messagebox.showinfo("Thành công", f"Giao dịch đã được thêm vào block #{index}")
    entry_sender.delete(0, tk.END)
    entry_receiver.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

def mine_block():
    previous_block = my_blockchain.get_previous_block()
    previous_proof = previous_block.proof
    proof = my_blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block.hash
    my_blockchain.add_transaction("Network", "Miner", 1)
    block = my_blockchain.create_block(proof, previous_hash)
    messagebox.showinfo("Thành công", f"Đã đào được block #{block.index}")
    display_chain()

def display_chain():
    output.delete("1.0", tk.END)
    for block in my_blockchain.chain:
        output.insert(tk.END, f"Block #{block.index}\n")
        output.insert(tk.END, f"Timestamp: {block.timestamp}\n")
        output.insert(tk.END, f"Transactions: {block.transactions}\n")
        output.insert(tk.END, f"Proof: {block.proof}\n")
        output.insert(tk.END, f"Previous Hash: {block.previous_hash}\n")
        output.insert(tk.END, f"Hash: {block.hash}\n")
        output.insert(tk.END, "-"*50 + "\n")

def check_validity():
    valid = my_blockchain.is_chain_valid(my_blockchain.chain)
    if valid:
        messagebox.showinfo("Hợp lệ", "Chuỗi blockchain hợp lệ.")
    else:
        messagebox.showerror("Không hợp lệ", "Blockchain đã bị thay đổi!")

# Giao diện chính
root = tk.Tk()
root.title("Blockchain UI")
root.geometry("600x650")

# Giao dịch
tk.Label(root, text="Người gửi:").pack()
entry_sender = tk.Entry(root, width=40)
entry_sender.pack()

tk.Label(root, text="Người nhận:").pack()
entry_receiver = tk.Entry(root, width=40)
entry_receiver.pack()

tk.Label(root, text="Số tiền:").pack()
entry_amount = tk.Entry(root, width=40)
entry_amount.pack()

tk.Button(root, text="Thêm giao dịch", command=add_transaction).pack(pady=5)
tk.Button(root, text="Đào block mới", command=mine_block).pack(pady=5)
tk.Button(root, text="Hiển thị blockchain", command=display_chain).pack(pady=5)
tk.Button(root, text="Kiểm tra tính hợp lệ", command=check_validity).pack(pady=5)

# Vùng hiển thị blockchain
output = scrolledtext.ScrolledText(root, width=70, height=20)
output.pack(pady=10)

root.mainloop()
