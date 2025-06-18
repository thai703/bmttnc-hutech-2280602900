import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ex01'))

from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher
from cipher.transposition.transposition_cipher import TranspositionCipher

app = Flask(__name__)

# routes for home page
@app.route('/')
def home():
    return render_template('index.html')

# ------------------ Caesar Cipher ------------------ #
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

# ------------------ Vigenère Cipher ------------------ #
@app.route('/vigenere')
def vigenere_page():
    return render_template('vigenere.html')

@app.route('/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    vigenere = VigenereCipher()
    encrypted_text = vigenere.vigenere_encrypt(text, key)
    return f"TEXT: {text}<br/>KEY: {key}<br/>ENCRYPTED TEXT: {encrypted_text}"

@app.route('/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    vigenere = VigenereCipher()
    decrypted_text = vigenere.vigenere_decrypt(text, key)
    return f"TEXT: {text}<br/>KEY: {key}<br/>DECRYPTED TEXT: {decrypted_text}"

# ------------------ Rail Fence Cipher ------------------ #
@app.route('/railfence')
def railfence_page():
    return render_template('railfence.html')

@app.route('/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    railfence = RailFenceCipher()
    encrypted_text = railfence.rail_fence_encrypt(text, key)
    return f"TEXT: {text}<br/>KEY: {key}<br/>ENCRYPTED TEXT: {encrypted_text}"

@app.route('/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    railfence = RailFenceCipher()
    decrypted_text = railfence.rail_fence_decrypt(text, key)
    return f"TEXT: {text}<br/>KEY: {key}<br/>DECRYPTED TEXT: {decrypted_text}"

# ------------------ Playfair Cipher ------------------ #
@app.route('/playfair')
def playfair_page():
    return render_template('playfair.html')

@app.route('/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    playfair = PlayfairCipher()
    matrix = playfair.create_playfair_matrix(key)
    encrypted_text = playfair.playfair_encrypt(text, matrix)
    return f"TEXT: {text}<br/>KEY: {key}<br/>ENCRYPTED TEXT: {encrypted_text}"

@app.route('/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    playfair = PlayfairCipher()
    matrix = playfair.create_playfair_matrix(key)
    decrypted_text = playfair.playfair_decrypt(text, matrix)
    return f"TEXT: {text}<br/>KEY: {key}<br/>DECRYPTED TEXT: {decrypted_text}"

# ------------------ Transposition Cipher ------------------ #
@app.route('/transposition')
def transposition_page():
    return render_template('transposition.html')

@app.route('/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    transposition = TranspositionCipher()
    encrypted_text = transposition.encrypt(text, key)
    return f"TEXT: {text}<br/>KEY: {key}<br/>ENCRYPTED TEXT: {encrypted_text}"

@app.route('/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    transposition = TranspositionCipher()
    decrypted_text = transposition.decrypt(text, key)
    return f"TEXT: {text}<br/>KEY: {key}<br/>DECRYPTED TEXT: {decrypted_text}"

# ----------------------------------------------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
