from SHA_2 import SHA_2
from RSA import RSA
from Cryptodome.Signature import pkcs1_15
import Helper
import Constants


class Signature:
    """
    Class Signature represents digital signature.
    It combines hashing and the asymmetric algorithm.
    """
    def __init__(self, sha_type, rsa_key_size, message):
        """
        Initialization method.
        :param sha_type: type of the hash method
        :param rsa_key_size: key size for the asymmetric algorithm
        :param message: message
        """
        self._sha = sha_type
        self._message = message
        self._rsa_key = rsa_key_size
        # rsa object
        self._rsa = None
        # signature
        self._signature = None

    def sign(self):
        """
        Signing method.
        :return: signature
        """
        _hash = SHA_2(self._sha, self._message).hash()
        rsa = RSA(self._rsa_key, None)
        self._rsa = rsa
        # sign
        signature = pkcs1_15.new(self._rsa.private_key).sign(_hash)
        # write signature to the file
        Helper.write_signature(['SHA-2', 'RSA'], [hex(int(self._sha)), hex(self._rsa.private_key.size_in_bits())], signature, Constants.signature_path)
        self._signature = signature

    def verify(self):
        """
        Check if the signature is valid.
        """
        _hash = SHA_2(self._sha, self._message).hash()
        try:
            pkcs1_15.new(self._rsa.private_key).verify(_hash, self._signature)
            return "Digital signature is valid!"
        except ValueError:
            return "Digital signature is not valid!"
