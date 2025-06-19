# rsa_cipher.py
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

class RSACipher:
    def __init__(self):
        pass

    def generate_keys(self):
        key = RSA.generate(2048)
        private_key = key.export_key().decode()
        public_key = key.publickey().export_key().decode()
        return private_key, public_key

    def sign(self, message, private_key_pem):
        private_key = RSA.import_key(private_key_pem)
        h = SHA256.new(message.encode())
        signature = pkcs1_15.new(private_key).sign(h)
        return base64.b64encode(signature).decode()

    def verify(self, message, signature_b64, public_key_pem):
        try:
            public_key = RSA.import_key(public_key_pem)
            h = SHA256.new(message.encode())
            signature = base64.b64decode(signature_b64)
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
