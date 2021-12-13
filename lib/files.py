from lib import aes_gcm
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from os import path


def extractName(filepath):
    return filepath.split(path.sep)[-1]


def replace_filename(filepath, filename):
    splittedFilepath = filepath.split(path.sep)
    splittedFilepath.pop()
    splittedFilepath.extend([filename])

    return path.sep.join(splittedFilepath)


def encryptFile(key, salt, filepath):
    filename = extractName(filepath)
    random_filename = SHA256.new(get_random_bytes(32)).digest().hex()

    encrypted_file_path = replace_filename(filepath, random_filename)
    encrypted_file = open(encrypted_file_path, "w")

    decrypted_file = open(filepath, 'r')
    file_content = decrypted_file.read()
    content_to_encrypt = "/".join([filename, file_content])

    encrypted_content = aes_gcm.encrypt(key, content_to_encrypt, salt)
    encrypted_file.write(encrypted_content)

    decrypted_file.close()
    encrypted_file.close()


def decryptFile(key, salt, filepath):
    decrypted_file = None

    encrypted_file = open(filepath, 'r')
    encrypted_content = encrypted_file.read()

    decrypted_content = aes_gcm.decrypt(key, encrypted_content, salt)
    separator_index = decrypted_content.find('/')
    filename = decrypted_content[:separator_index]
    file_content = decrypted_content[separator_index + 1:]

    decrypted_filepath = replace_filename(filepath, filename)
    decrypted_file = open(decrypted_filepath, 'w')
    decrypted_file.write(file_content)

    decrypted_file.close()
    encrypted_file.close()


def saveKeys(filepath, key, salt):
    keysFile = open(filepath, 'w')
    keysFile.write(key.hex())
    keysFile.write('\n')
    keysFile.write(salt.hex())
    keysFile.close()
