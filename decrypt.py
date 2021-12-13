from lib import files
from os import path, listdir, remove
from Crypto.Random import get_random_bytes

keyspath = path.join(
    'key-salt.txt'
)

keysFile = open(keyspath, 'r')


key = bytes.fromhex(keysFile.readline().rstrip())
salt = bytes.fromhex(keysFile.readline())


def decryptDir(dir):
    for filename in listdir(dir):
        filepath = path.join(dir, filename)

        if (path.isdir(filepath)):
            decryptDir(filepath)
            continue

        files.decryptFile(key, salt, filepath)
        remove(filepath)

    remove(keyspath)


decryptDir('file_tree')
