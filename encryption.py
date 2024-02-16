from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


class EncryptionManager:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        """
        Encrypts plaintext using AES encryption.
        Returns the initialization vector (IV) and the ciphertext.
        """
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    def decrypt(self, iv, ciphertext):
        """
        Decrypts ciphertext using AES encryption.
        Requires the initialization vector (IV).
        """
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ciphertext)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
