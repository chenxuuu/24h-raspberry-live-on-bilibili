import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):
    """
    A classical AES Cipher. Can use any size of data and any size of password thanks to padding.
    Also ensure the coherence and the type of the data with a unicode to byte converter.
    """
    def __init__(self, key):
        self.bs = 16
        self.key = AESCipher.strToBytes(key)

    @staticmethod
    def strToBytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.strToBytes(chr(self.bs - len(s) % self.bs))

    def encrypt(self, raw, iv):
        raw = self.pad(AESCipher.strToBytes(raw))
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(raw)).decode('utf-8')
