import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ex01'))

from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher


app = Flask(__name__)

#routes for home page
@app.route('/')
def home():
    return render_template('index.html')

#routes for caesar cypher
@app.route('/caesar')
def caesar():
    return render_template('caesar.html')

@app.route('/encrypt', methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt(text, key)
    return f"TEXT: {text}<br/>KEY: {key}<br/>ENCRYPTED TEXT: {encrypted_text}"

@app.route('/decrypt', methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt(text, key)
    return f"TEXT: {text}<br/>KEY: {key}<br/>DECRYPTED TEXT: {decrypted_text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)