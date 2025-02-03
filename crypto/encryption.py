from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

class Encryption:
    def __init__(self, key):
        """
        Initializes the encryption class with the provided key.
        AES requires the key to be 16, 24, or 32 bytes long.
        """
        if len(key) not in [16, 24, 32]:
            raise ValueError("AES key must be either 16, 24, or 32 bytes long.")
        self.key = key

    def encrypt_message(self, iv, data):
        """
        Encrypts the plaintext using AES encryption in CBC mode.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))  # Pad the data to block size and encrypt
        return ciphertext  # Return both IV and ciphertext

    def decrypt_message(self, iv, ciphertext):
        """
        Decrypts the ciphertext using AES decryption in CBC mode.
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)  # AES.block_size is 16
        return plaintext

    def generate_salt(self):
        """
        Generates a random salt for key derivation.
        """
        return os.urandom(16)
