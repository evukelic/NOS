from Envelope import Envelope
from Signature import Signature


class Seal:
    """
    Class Seal represents digital seal.
    It combines digital envelope and digital signature.
    """
    def __init__(self, encryption_algorithm, key_type, rsa_key_size, message, mode, sha_type):
        """
        Initialization method.
        :param encryption_algorithm: which symmetric algorithm will be used
        :param key_type: key size for the symmetric algorithm
        :param rsa_key_size: key size for the asymmetric algorithm
        :param message: encryption data
        :param mode: mode of the symmetric algorithm
        :param sha_type: SHA-2 type
        """
        self._sha = sha_type
        self._rsa_key = rsa_key_size
        # generate envelope
        self._envelope = Envelope(encryption_algorithm, key_type, rsa_key_size, message, mode)
        self._signature = None
        # envelope encryption result
        self._env_res = None

    def seal(self):
        """
        Seal method.
        """
        self._env_res = self._envelope.encrypt()
        message = str(self._envelope.cipher) + str(self._envelope.crypt_key)
        self._signature = Signature(self._sha, self._rsa_key, message)
        self._signature.sign()

    def unseal(self):
        """
        Unseal method.
        :return: original message
        """
        msg = self._envelope.decrypt(self._env_res)
        # verifies the signature
        verification = self._signature.verify()
        return msg, verification



