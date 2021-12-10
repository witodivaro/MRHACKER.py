from lib import files
from os import path, listdir, remove
from Crypto.Random import get_random_bytes

keyspath = path.join(
    'key-salt.txt'
)

keysFile = open(keyspath, 'r')


key = bytes.fromhex(keysFile.readline().rstrip())
salt = bytes.fromhex(keysFile.readline())

for filename in listdir('files'):
    filepath = path.join('files', filename)
    files.decryptFile(key, salt, filepath)
    remove(filepath)
    remove(keyspath)
