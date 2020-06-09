import base64
import re

"""
Helper file with static methods for writing in the files.
"""


def get_header(file):
    """
    Write the header of the file.
    :param file: file
    """
    file.write('---BEGIN OS2 CRYPTO DATA---\n\nDescription:\n')


def get_footer(file):
    """
    Write the footer of the file.
    :param file: file
    """
    file.write('\n---END OS2 CRYPTO DATA---\n')


def get_method(methods, file):
    """
    Write out all the methods.
    :param methods: List of methods
    :param file: file
    """
    file.write('\nMethod:\n')
    for m in methods:
        line = '    ' + m + '\n'
        file.write(line)
    file.write('\n')


def get_key_length(key_lens, file):
    """
    Write out the key lengths for the given keys.
    :param key_lens: List of key lengths
    :param file: file
    """
    file.write('Key length:\n')
    for k in key_lens:
        line = '    ' + '{0:04x}'.format(int(k, 0)) + '\n'
        file.write(line)
    file.write('\n')


def split_data(data, file, decode=False):
    """
    Split the data after 60 characters and write it in the file.
    :param data: data for splitting
    :param file: file
    :param decode: should data be decoded?
    """
    if decode:
        line = '    ' + re.sub("(.{60})", "\\1\n    ", data.decode('ascii'), 0, re.DOTALL) + '\n'
        file.write(line)
    else:
        line = '    ' + re.sub("(.{60})", "\\1\n    ", data, 0, re.DOTALL) + '\n'
        file.write(line)


def write_data_to_file(methods, data, iv, path):
    """
    Write crypt data to the file.
    :param methods: list of methods
    :param data: crypt data
    :param iv: initialization vector
    :param path: path to the file
    """
    file = open(path, "w")
    get_header(file)
    file.write('    Crypted file\n')
    get_method(methods, file)
    if iv is not None:
        file.write('Initialization vector:\n')
        line = '    ' + iv + '\n'
        file.write(line)
        file.write('\n')
    file.write('Data:\n')
    split_data(data, file, True)
    get_footer(file)


def write_secret_key_to_file(methods, key, file):
    """
    Write secret key to the file.
    :param methods: list of methods
    :param key: key for the key length
    :param file: path to the file
    """
    file = open(file, "w")
    get_header(file)
    file.write('    Secret key\n')
    get_method(methods, file)
    get_key_length([str(hex(len(key)*8))], file)
    file.write('Secret key:\n')
    line = '    ' + key.hex() + '\n'
    file.write(line)
    get_footer(file)


def write_rsa_key(key, path, private=True):
    """
    Write out the RSA key.
    :param key: key
    :param path: path to the file
    :param private: is key private or public?
    """
    file = open(path, "w")
    get_header(file)
    file.write('    Private key\n')
    get_method(['RSA'], file)
    get_key_length([hex(key.size_in_bits())], file)
    file.write('Modulus:\n')
    mod = hex(key.n)
    split_data(mod[2:], file)
    if private:
        file.write('\nPrivate exponent:\n')
        pex = hex(key.d)
    else:
        file.write('\nPublic exponent:\n')
        pex = hex(key.e)
    split_data(pex[2:], file)
    get_footer(file)


def write_envelope(methods, keys, data, crypt_key, path):
    """
    Write out the envelope file.
    :param methods: list of methods
    :param keys: list of keys for the key length
    :param data: data to be written
    :param crypt_key: crypt key
    :param path: path to the file
    """
    file = open(path, "w")
    get_header(file)
    file.write('    Envelope\n')
    get_method(methods, file)
    lens = []
    for k in keys:
        lens.append(str(hex(len(k)*8)))
    get_key_length(lens, file)
    file.write('Envelope data:\n')
    split_data(data, file, True)
    file.write('\nEnvelope crypt key:\n')
    split_data(crypt_key, file)
    get_footer(file)


def write_signature(methods, keys, signature, path):
    """
    Write signature to the file.
    :param methods: list of methods
    :param keys: list of keys for the key length
    :param signature: signature
    :param path: path to the file
    """
    file = open(path, "w")
    get_header(file)
    file.write('    Signature\n')
    get_method(methods, file)
    get_key_length(keys, file)
    file.write('Signature:\n')
    split_data(base64.b64encode(signature).hex(), file)
    get_footer(file)


def read_dict(path):
    """
    Generate dictionary from the json-like format files.
    :param path: path to the file
    :return: dictionary
    """
    file = open(path, "r")
    _dict = {}
    key = None
    value = None
    while True:
        line = file.readline()
        if not line:
            continue
        elif line.strip() == '---BEGIN OS2 CRYPTO DATA---':
            continue
        elif line.strip() == '---END OS2 CRYPTO DATA---':
            break

        if line.strip().endswith(":"):
            key = line.strip()[:-1]
        else:
            value = line.strip()

        if key and value:
            _dict[key] = value
            key = None
            value = None

    return _dict
