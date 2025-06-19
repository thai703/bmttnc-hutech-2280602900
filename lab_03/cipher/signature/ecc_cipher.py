# ecc_cipher.py
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import base64

class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        key = ECC.generate(curve='P-256')
        private_key = key.export_key(format='PEM')
        public_key = key.public_key().export_key(format='PEM')
        return private_key, public_key

    def sign(self, message, private_key_pem):
        private_key = ECC.import_key(private_key_pem)
        h = SHA256.new(message.encode())
        signer = DSS.new(private_key, 'fips-186-3')
        signature = signer.sign(h)
        return base64.b64encode(signature).decode()

    def verify(self, message, signature_b64, public_key_pem):
        try:
            public_key = ECC.import_key(public_key_pem)
            h = SHA256.new(message.encode())
            verifier = DSS.new(public_key, 'fips-186-3')
            signature = base64.b64decode(signature_b64)
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
