# rail_fence_app.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rail_fence import Ui_MainWindow
from cipher.rail_fence.rail_fence_cipher import RailFenceCipher

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Gán nút
        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

        # Tạo đối tượng mã hóa
        self.cipher = RailFenceCipher()

    def encrypt_text(self):
        plain_text = self.ui.txt_plaintext.toPlainText()
        num_rails_str = self.ui.txt_numrails.text()


        if not plain_text or not num_rails_str:
            QMessageBox.warning(self, "Warning", "Please enter both Plain Text and Number of Rails!")
            return

        try:
            num_rails = int(num_rails_str)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Number of Rails must be an integer!")
            return

        encrypted = self.cipher.rail_fence_encrypt(plain_text, num_rails)
        self.ui.txt_ciphertext.setPlainText(encrypted)

    def decrypt_text(self):
        cipher_text = self.ui.txt_ciphertext.toPlainText()
        num_rails_str = self.ui.txt_numrails.text()

        if not cipher_text or not num_rails_str:
            QMessageBox.warning(self, "Warning", "Please enter both Cipher Text and Number of Rails!")
            return

        try:
            num_rails = int(num_rails_str)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Number of Rails must be an integer!")
            return

        decrypted = self.cipher.rail_fence_decrypt(cipher_text, num_rails)
        self.ui.txt_plaintext.setPlainText(decrypted)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
