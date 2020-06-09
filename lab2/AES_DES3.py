from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import DES3
from Cryptodome.Util.Padding import pad, unpad

import base64
import Constants
import Helper


def get_mode(mode, aes):
    """
    Static method which returns mode for the chosen algorithm.
    """
    if mode == 'ECB':
        if aes:
            return AES.MODE_ECB
        else:
            return DES3.MODE_ECB
    else:
        if aes:
            return AES.MODE_CBC
        else:
            return DES3.MODE_CBC


def get_key_type(key_type):
    """
    Generate key type from the bit to byte format.
    :param key_type: Key as bits
    :param aes: True if AES, false if DES
    :return: Key as bytes
    """
    if key_type == '128' or key_type == '112':
        return 16
    elif key_type == '192' or key_type == '168':
        return 24
    else:
        return 32


def get_block_size(aes):
    """
    Return block size for the wanted algorithm.
    :param aes: True if AES, false if DES
    :return: Block size
    """
    if aes:
        return AES.block_size
    else:
        return DES3.block_size


def get_iv(mode, block):
    """
    Return init vector if needed.
    :param mode: ECB or CBC
    :param block: block size
    :return: Init vector if needed, None otherwise
    """
    if mode == 'ECB':
        return None
    else:
        return Random.get_random_bytes(block)


def get_iv_hex(iv):
    """
    Transform initialization vector to hexadecimal value.
    :param iv: Init vector
    :return: Hex or None
    """
    if iv is not None:
        return iv.hex()
    else:
        return None


class AES_DES3:
    """
    Class AES3DES gives methods for encryption and decryption of wanted message,
    based on the given mode and type of the key.
    """
    def __init__(self, key_type, message, mode, default=True):
        """
        Initializes an object.
        :param key_type: Type of the key (128, 192 or 256 bits)
        :param message: Message which will be encrypted/decrypted
        :param mode: Mode of an algorithm
        :param default: AES or DES3
        """
        self._key_type = get_key_type(key_type)
        self._message = message
        self._mode = get_mode(mode, default)
        self._block = get_block_size(default)
        self._iv = get_iv(mode, self._block)
        self._iv_hex = get_iv_hex(self._iv)
        self._aes = default
        self._key_hex = None

    def generate_alg(self, key, aes):
        """
        Generate algorithm for given key size and algorithm type.
        :param key: Secret key
        :param aes: True if AES, false if DES3
        :return: Algorithm instance
        """
        if self._iv is not None:
            if aes:
                return AES.new(key=key, mode=self._mode, IV=self._iv)
            else:
                return DES3.new(key=key, mode=self._mode, IV=self._iv)
        else:
            if aes:
                return AES.new(key=key, mode=self._mode)
            else:
                return DES3.new(key=key, mode=self._mode)

    def encrypt(self):
        """
        Encryption method.
        :return: Generated secret key, encrypted message
        """
        if self._aes:
            methods = ['AES']
        else:
            methods = ['DES3']

        key = Random.get_random_bytes(self._key_type)
        if self._aes:
            self._key_hex = key.hex()
        else:
            self._key_hex = DES3.adjust_key_parity(key)

        # Write generated secret key to a file
        if self._aes:
            Helper.write_secret_key_to_file(methods, key, Constants.aes_secret_key_path)
        else:
            Helper.write_secret_key_to_file(methods, key, Constants.des3_secret_key_path)

        alg = self.generate_alg(key, self._aes)

        cipher = alg.encrypt(pad(str.encode(self._message), self._block))
        if self._aes:
            Helper.write_data_to_file(methods, base64.b64encode(cipher), self._iv_hex, Constants.aes_crypted_file_path)
        else:
            Helper.write_data_to_file(methods, base64.b64encode(cipher), self._iv_hex, Constants.des3_crypted_file_path)
        return key, cipher

    def decrypt(self, key, cipher):
        """
        Decryption method.
        :param key: Generated secret key
        :param cipher: Encrypted message
        :return: Decrypted message
        """
        alg = self.generate_alg(key, self._aes)
        dec = unpad(alg.decrypt(cipher), self._block)
        return dec.decode()
