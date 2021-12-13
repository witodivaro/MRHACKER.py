from lib import files
from os import path, listdir, remove
from Crypto.Random import get_random_bytes

keyspath = path.join(
    'key-salt.txt'
)

keysFile = open(keyspath, 'r')


key = bytes.fromhex(keysFile.readline().rstrip())
salt = bytes.fromhex(keysFile.readline())


def decrypt_dir(dir):
    for filename in listdir(dir):
        filepath = path.join(dir, filename)

        if (path.isdir(filepath)):
            decrypt_dir(filepath)
            continue

        files.decrypt_file(key, salt, filepath)
        remove(filepath)


decrypt_dir('file_tree')
remove(keyspath)
