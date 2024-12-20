from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  
from cryptography.hazmat.primitives import hashes  
from cryptography.hazmat.backends import default_backend  
from base64 import b64encode, b64decode  
import os  
from src.constants import Constant as con


  
def encrypt_data(key, data):  
    if data is None:
        return None
    iv = os.urandom(16)  
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())  
    encryptor = cipher.encryptor()  
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()  
    return b64encode(iv + encrypted_data).decode('utf-8')  
  
def decrypt_data(key, data):  
    if data is None:
        return None
    data = b64decode(data.encode('utf-8'))  
    iv = data[:16]  
    encrypted_data = data[16:]  
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())  
    decryptor = cipher.decryptor()  
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()  
    return decrypted_data.decode('utf-8')  