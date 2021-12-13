import codecs

from lib import aes_gcm, strings, encodings
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from os import path


def read_file(filepath):
    for encoding in encodings.encodings:
        try:
            return codecs.open(filepath, 'r', encoding).read(), encoding
        except UnicodeDecodeError:
            pass


def extract_name(filepath):
    return filepath.split(path.sep)[-1]


def replace_filename(filepath, filename):
    splittedFilepath = filepath.split(path.sep)
    splittedFilepath.pop()
    splittedFilepath.extend([filename])

    return path.sep.join(splittedFilepath)


def encrypt_file(key, salt, filepath):
    filename = extract_name(filepath)
    random_filename = SHA256.new(get_random_bytes(32)).digest().hex()

    encrypted_file_path = replace_filename(filepath, random_filename)
    encrypted_file = open(encrypted_file_path, "w")

    (file_content, encoding) = read_file(filepath)
    content_to_encrypt = "/".join([encoding, filename, file_content])

    encrypted_content = aes_gcm.encrypt(key, content_to_encrypt, salt)
    encrypted_file.write(encrypted_content)

    encrypted_file.close()


def decrypt_file(key, salt, filepath):
    decrypted_file = None

    encrypted_file = open(filepath, 'r')
    encrypted_content = encrypted_file.read()

    decrypted_content = aes_gcm.decrypt(key, encrypted_content, salt)
    separators = list(strings.find_all(decrypted_content, '/'))

    encoding = decrypted_content[:separators[0]]
    filename = decrypted_content[separators[0] + 1:separators[1]]
    file_content = decrypted_content[separators[1] + 1:]

    encoded_file_content = file_content.encode(encoding)

    decrypted_filepath = replace_filename(filepath, filename)
    decrypted_file = open(decrypted_filepath, 'wb')
    decrypted_file.write(encoded_file_content)

    decrypted_file.close()
    encrypted_file.close()


def save_keys(filepath, key, salt):
    keysFile = open(filepath, 'w')
    keysFile.write(key.hex())
    keysFile.write('\n')
    keysFile.write(salt.hex())
    keysFile.close()
