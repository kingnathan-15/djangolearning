from pathlib import Path
import hashlib, hmac
from Crypto.Cipher import AES
from abc import ABC, abstractmethod

class CoreEncryption(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def encrypt_passwords(self, plaintext:str):
        pass
    
    @abstractmethod
    def decrypt_passwords(self, ciphertext:str):
        pass


class AESEncryption(CoreEncryption):
    def __init__(self, master_path = "master.txt"):

        file_path = Path(master_path)
        if file_path.is_file():
            self.status = True
        else:
            self.status = False

    # #Writes an input master password to a file after a hash
    # def create_master_password(self, password_string):
    #     salt = b"my_salt_value"
    #     key = hashlib.pbkdf2_hmac("sha256", password_string.encode("utf-8"), salt, 100000)
    #     with open("master.txt", "w") as f:
    #         f.write(key.hex())
    #     return key
    
    # #Verifies the master password by comparing it to a hash
    # def verify_master_password(self, password_string):
    #     salt = b"my_salt_value"
    #     key = hashlib.pbkdf2_hmac("sha256", password_string.encode("utf-8"), salt, 100000)
    #     with open("master.txt", "r") as f:
    #         stored_key = f.read()
    #     if key.hex() == stored_key:
    #         self.master_password = stored_key
    #         return True
    #     else:
    #         return False
    
    # #Processes a plaintext password and outputs a hexadecimal blob consisting of a nonce, a tag, and a ciphertext
    def encrypt_passwords(self, master, password_string):
        key = hashlib.sha256(master.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(password_string.encode())
        blob = cipher.nonce+tag+ciphertext
        return blob.hex()
    
    #Processes the encrypted blob and outputs the plaintext string
    def decrypt_passwords(self,master, blob):
        if isinstance(blob, str):
            blob = bytes.fromhex(blob)
        nonce = blob[:16]
        tag = blob[16:32]
        ciphertext = blob[32:]
        key = hashlib.sha256(master.encode()).digest()
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data.decode()
    
    