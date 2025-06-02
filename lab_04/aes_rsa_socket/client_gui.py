import tkinter as tk
from tkinter import messagebox, scrolledtext
import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client - AES/RSA")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Socket and crypto variables
        self.client_socket = None
        self.aes_key = None
        self.client_key = None
        self.running = False

        # GUI components
        self.create_widgets()

        # Start connection
        self.connect_to_server()

    def create_widgets(self):
        # Status frame
        status_frame = tk.Frame(self.root, bg="#f0f0f0")
        status_frame.pack(pady=5, fill=tk.X)
        self.status_label = tk.Label(
            status_frame,
            text="Disconnected",
            fg="red",
            bg="#f0f0f0",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack()

        # Chat display with scrollbar
        chat_frame = tk.Frame(self.root, bg="#f0f0f0")
        chat_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            height=20,
            width=60,
            state='disabled',
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True)

        # Message entry
        entry_frame = tk.Frame(self.root, bg="#f0f0f0")
        entry_frame.pack(pady=5, fill=tk.X, padx=10)
        self.message_entry = tk.Entry(
            entry_frame,
            width=50,
            font=("Arial", 10)
        )
        self.message_entry.pack(side=tk.LEFT, padx=5)
        self.message_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(
            entry_frame,
            text="Send",
            command=self.send_message,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Disconnect button
        self.disconnect_button = tk.Button(
            self.root,
            text="Disconnect",
            command=self.disconnect,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.disconnect_button.pack(pady=5)

    def connect_to_server(self):
        try:
            # Initialize client socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))

            # Generate RSA key pair
            self.client_key = RSA.generate(2048)

            # Receive server's public key
            server_public_key = RSA.import_key(self.client_socket.recv(2048))

            # Send client's public key to the server
            self.client_socket.send(self.client_key.publickey().export_key(format='PEM'))

            # Receive encrypted AES key from the server
            encrypted_aes_key = self.client_socket.recv(2048)

            # Decrypt the AES key using client's private key
            cipher_rsa = PKCS1_OAEP.new(self.client_key)
            self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)

            # Update status
            self.status_label.config(text="Connected", fg="green")
            self.running = True

            # Start receiving messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.status_label.config(text="Disconnected", fg="red")

    def encrypt_message(self, message):
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def decrypt_message(self, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_message.decode()

    def receive_messages(self):
        while self.running:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = self.decrypt_message(encrypted_message)
                self.display_message(f"Other: {decrypted_message}")
            except Exception as e:
                if self.running:
                    self.display_message(f"Error: {e}")
                    self.disconnect()
                break

    def send_message(self, event=None):
        if not self.running:
            messagebox.showwarning("Warning", "Not connected to server")
            return

        message = self.message_entry.get().strip()
        if message:
            try:
                encrypted_message = self.encrypt_message(message)
                self.client_socket.send(encrypted_message)
                self.display_message(f"You: {message}")
                self.message_entry.delete(0, tk.END)
                if message == "exit":
                    self.disconnect()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")
                self.disconnect()

    def display_message(self, message):
        self.chat_text.config(state='normal')
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.config(state='disabled')
        self.chat_text.see(tk.END)

    def disconnect(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        self.status_label.config(text="Disconnected", fg="red")
        self.client_socket = None

    def on_closing(self):
        self.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()