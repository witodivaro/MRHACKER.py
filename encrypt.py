from lib import files
from os import path, listdir, remove
from Crypto.Random import get_random_bytes

keyspath = path.join(
    'key-salt.txt'
)

key = get_random_bytes(16)
salt = get_random_bytes(16)

for filename in listdir('files'):
    filepath = path.join('files', filename)
    files.encryptFile(key, salt, filepath)
    remove(filepath)


files.saveKeys(keyspath, key, salt)
