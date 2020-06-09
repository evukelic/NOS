from Cryptodome.Hash import SHA224
from Cryptodome.Hash import SHA256


class SHA_2:
    """
    Class SHA_2 represents class used for hashing the data by either SHA224 or SHA256.
    """
    def __init__(self, key_type, message):
        """
        Initialization method.
        :param key_type: SHA-2 type
        :param message: message
        """
        self._keyType = key_type
        self._message = message

    def hash(self):
        """
        Hashing method. Hashes based on a key type.
        :return: hashed data
        """
        if self._keyType == '256':
            return SHA224.new(data=str.encode(self._message))
        else:
            return SHA256.new(data=str.encode(self._message))
