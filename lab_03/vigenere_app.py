# vigenere_app.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.vigenere import Ui_MainWindow
from cipher.vigenere.vigenere_cipher import VigenereCipher

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Gán nút
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

        # Tạo đối tượng mã hóa
        self.cipher = VigenereCipher()

    def encrypt_text(self):
        plain_text = self.ui.txt_plaintext.toPlainText()
        key = self.ui.txt_key.toPlainText()

        if not plain_text or not key:
            QMessageBox.warning(self, "Warning", "Please enter both Plain Text and Key!")
            return

        encrypted = self.cipher.vigenere_encrypt(plain_text, key)
        self.ui.txt_ciphertext.setPlainText(encrypted)

    def decrypt_text(self):
        cipher_text = self.ui.txt_ciphertext.toPlainText()
        key = self.ui.txt_key.toPlainText()

        if not cipher_text or not key:
            QMessageBox.warning(self, "Warning", "Please enter both Cipher Text and Key!")
            return

        decrypted = self.cipher.vigenere_decrypt(cipher_text, key)
        self.ui.txt_plaintext.setPlainText(decrypted)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
