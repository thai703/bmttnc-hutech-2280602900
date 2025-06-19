# transposition_app.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.transposition import Ui_MainWindow
from cipher.transposition.transposition_cipher import TranspositionCipher

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cipher = TranspositionCipher()

        # Kết nối nút
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        plain_text = self.ui.txt_plaintext.toPlainText()
        key_str = self.ui.txt_key.text()

        if not key_str.isdigit():
            QMessageBox.warning(self, "Error", "Key must be an integer.")
            return

        key = int(key_str)
        cipher_text = self.cipher.encrypt(plain_text, key)
        self.ui.txt_ciphertext.setPlainText(cipher_text)

    def decrypt_text(self):
        cipher_text = self.ui.txt_ciphertext.toPlainText()
        key_str = self.ui.txt_key.text()

        if not key_str.isdigit():
            QMessageBox.warning(self, "Error", "Key must be an integer.")
            return

        key = int(key_str)
        plain_text = self.cipher.decrypt(cipher_text, key)
        self.ui.txt_plaintext.setPlainText(plain_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
