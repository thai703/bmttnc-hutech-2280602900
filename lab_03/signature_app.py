# signature_app.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.signature import Ui_MainWindow
from cipher.signature.rsa_cipher import RSACipher
from cipher.signature.ecc_cipher import ECCCipher

class SignatureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.rsa_cipher = RSACipher()
        self.ecc_cipher = ECCCipher()

        # RSA Events
        self.ui.btn_genkey_rsa.clicked.connect(self.generate_rsa_keys)
        self.ui.btn_sign_rsa.clicked.connect(self.sign_rsa)
        self.ui.btn_verify_rsa.clicked.connect(self.verify_rsa)

        # ECC Events
        self.ui.btn_genkey_ecc.clicked.connect(self.generate_ecc_keys)
        self.ui.btn_sign_ecc.clicked.connect(self.sign_ecc)
        self.ui.btn_verify_ecc.clicked.connect(self.verify_ecc)

    # RSA Methods
    def generate_rsa_keys(self):
        private_key, public_key = self.rsa_cipher.generate_keys()
        self.ui.txt_rsa_private_key.setPlainText(private_key)
        self.ui.txt_rsa_public_key.setPlainText(public_key)

    def sign_rsa(self):
        private_key = self.ui.txt_rsa_private_key.toPlainText()
        message = self.ui.txt_message.toPlainText()
        signature = self.rsa_cipher.sign(message, private_key)
        self.ui.txt_rsa_signature.setPlainText(signature)

    def verify_rsa(self):
        public_key = self.ui.txt_rsa_public_key.toPlainText()
        message = self.ui.txt_message.toPlainText()
        signature = self.ui.txt_rsa_signature.toPlainText()
        result = self.rsa_cipher.verify(message, signature, public_key)
        QMessageBox.information(self, "Verify RSA", "✅ Chữ ký hợp lệ!" if result else "❌ Chữ ký không hợp lệ!")

    # ECC Methods
    def generate_ecc_keys(self):
        private_key, public_key = self.ecc_cipher.generate_keys()
        self.ui.txt_ecc_private_key.setPlainText(private_key)
        self.ui.txt_ecc_public_key.setPlainText(public_key)

    def sign_ecc(self):
        private_key = self.ui.txt_ecc_private_key.toPlainText()
        message = self.ui.txt_message.toPlainText()
        signature = self.ecc_cipher.sign(message, private_key)
        self.ui.txt_ecc_signature.setPlainText(signature)

    def verify_ecc(self):
        public_key = self.ui.txt_ecc_public_key.toPlainText()
        message = self.ui.txt_message.toPlainText()
        signature = self.ui.txt_ecc_signature.toPlainText()
        result = self.ecc_cipher.verify(message, signature, public_key)
        QMessageBox.information(self, "Verify ECC", "✅ Chữ ký hợp lệ!" if result else "❌ Chữ ký không hợp lệ!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignatureApp()
    window.show()
    sys.exit(app.exec_())
