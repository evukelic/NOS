from Cryptodome.PublicKey import RSA as _RSA
from Cryptodome.Cipher import PKCS1_OAEP

import Helper
import base64
import Constants


class RSA:
    """
    Class RSA gives methods for encryption and decryption of wanted message,
    based on the given type of the key.
    """
    def __init__(self, key, message, as_bytes=False):
        """
        Initialization method.
        :param key: key size
        :param message: message for encryption
        :param as_bytes: should message be encoded?
        """
        self._key_size = key
        self._private_key = self.get_private_key()
        self._public_key = self.get_public_key()
        self._message = message
        self._bytes = as_bytes

    def get_private_key(self):
        """
        Generate private key and write it to the file.
        :return: private key
        """
        key = _RSA.generate(self._key_size)
        file = open(Constants.private_key_path, "wb")
        file.write(key.export_key())
        return key

    def get_public_key(self):
        """
        Generate public key and write it to the file.
        :return: public key
        """
        file = open(Constants.public_key_path, "wb")
        key = self._private_key.publickey()
        file.write(key.export_key())
        return key

    def encrypt(self):
        """
        Encrypt the data.
        :return: crypt data
        """
        Helper.write_rsa_key(self._private_key, Constants.rsa_private_key_path)
        Helper.write_rsa_key(self._public_key, Constants.rsa_public_key_path, False)
        if self._bytes:
            data = self._message
        else:
            data = self._message.encode("utf-8")
        enc = PKCS1_OAEP.new(self._public_key).encrypt(data)
        Helper.write_data_to_file(['RSA'], base64.b64encode(enc), None, Constants.rsa_crypted_file_path)
        return enc

    def decrypt(self, enc):
        """
        Decrypt the data.
        :param enc: crypt data
        :return: original message
        """
        return PKCS1_OAEP.new(self._private_key).decrypt(enc)

    @property
    def private_key(self):
        """
        Property getter.
        :return: private key
        """
        return self._private_key
