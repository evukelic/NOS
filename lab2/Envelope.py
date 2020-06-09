from AES_DES3 import AES_DES3
from RSA import RSA

import base64
import Constants
import Helper


class Envelope:
    """
    Class Envelope represents a digital envelope.
    It encrypts the data using both symmetric and asymmetric algorithms.
    """
    def __init__(self, encryption_algorithm, key_type, rsa_key_size, message, mode):
        """
        Initialization method.
        :param encryption_algorithm: which symmetric algorithm will be used
        :param key_type: key size for the symmetric algorithm
        :param rsa_key_size: key size for the asymmetric algorithm
        :param message: encryption data
        :param mode: mode of the symmetric algorithm
        """
        self._algorithm = encryption_algorithm
        self._key_type = key_type
        self._mode = mode
        self._message = message
        self._rsa_key = rsa_key_size
        # path to the envelope file
        self._path = None
        # crypt data
        self._cipher = None
        # crypt key
        self._crypt_key = None

    def encrypt(self):
        """
        Encryption method.
        :return: symmetric algorithm object
        """
        # message is encrypted by the given symmetric algorithm
        if self._algorithm == "AES":
            sym_alg = AES_DES3(self._key_type, self._message, self._mode)
            self._path = Constants.aes_secret_key_path
        else:
            sym_alg = AES_DES3(self._key_type, self._message, self._mode, False)
            self._path = Constants.des3_secret_key_path

        # encryption
        key, cipher = sym_alg.encrypt()
        self._cipher = cipher

        # key is encrypted by the RSA asymmetric algorithm
        rsa = RSA(self._rsa_key, key, True)
        crypt_key = rsa.encrypt()
        self._crypt_key = crypt_key
        Helper.write_envelope([self._algorithm, 'RSA'], [key, crypt_key], base64.b64encode(cipher), bytes.hex(crypt_key), Constants.envelope_path)

        return sym_alg

    def decrypt(self, alg):
        """
        Decryption algorithm.
        :param alg: symmetric algorithm
        :return: original data
        """
        # parse the file into the dictionary
        pairs = Helper.read_dict(self._path)
        # find key in dictionary
        key = pairs['Secret key']
        return alg.decrypt(bytes.fromhex(key), self._cipher)

    @property
    def cipher(self):
        """
        Cipher property getter.
        :return: cipher
        """
        return self._cipher

    @property
    def crypt_key(self):
        """
        Crypt key property getter.
        :return: crypt_key
        """
        return self._crypt_key
