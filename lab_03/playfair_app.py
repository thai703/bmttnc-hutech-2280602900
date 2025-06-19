# playfair_app.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_MainWindow
from cipher.playfair.playfair_cipher import PlayfairCipher

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cipher = PlayfairCipher()

        # Kết nối nút
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        plain_text = self.ui.txt_plaintext.toPlainText()
        key = self.ui.txt_key.toPlainText()

        if not key:
            QMessageBox.warning(self, "Error", "Please enter a key.")
            return

        matrix = self.cipher.create_playfair_matrix(key)
        cipher_text = self.cipher.playfair_encrypt(plain_text, matrix)
        self.ui.txt_ciphertext.setPlainText(cipher_text)

    def decrypt_text(self):
        cipher_text = self.ui.txt_ciphertext.toPlainText()
        key = self.ui.txt_key.toPlainText()

        if not key:
            QMessageBox.warning(self, "Error", "Please enter a key.")
            return

        matrix = self.cipher.create_playfair_matrix(key)
        plain_text = self.cipher.playfair_decrypt(cipher_text, matrix)
        self.ui.txt_plaintext.setPlainText(plain_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
