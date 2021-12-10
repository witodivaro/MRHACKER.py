from lib import aes_gcm
from Crypto.Random import get_random_bytes
from os import path


def extractName(filepath):
    return filepath.split(path.sep)[-1]


def replaceFilename(filepath, filename):
    splittedFilepath = filepath.split(path.sep)
    splittedFilepath.pop()
    splittedFilepath.extend([filename])

    return path.sep.join(splittedFilepath)


def encryptFile(key, salt, filepath):
    filename = extractName(filepath)
    encryptedFilename = aes_gcm.encrypt(key, filename, salt)

    encryptedFilepath = replaceFilename(filepath, encryptedFilename)
    encryptedFile = open(encryptedFilepath, "w")

    with open(filepath, 'r') as decryptedFile:
        for line in decryptedFile:
            encryptedLine = aes_gcm.encrypt(key, line, salt)
            encryptedFile.write(encryptedLine)
        decryptedFile.close()
        encryptedFile.close()


def decryptFile(key, salt, filepath):
    filename = extractName(filepath)

    decryptedFilename = aes_gcm.decrypt(key, filename, salt)
    decryptedFilepath = replaceFilename(filepath, decryptedFilename)

    decryptedFile = open(decryptedFilepath, 'w')

    with open(filepath, 'r') as encryptedFile:
        for line in encryptedFile:
            decryptedLine = aes_gcm.decrypt(key, line, salt)
            decryptedFile.write(decryptedLine)
        decryptedFile.close()
        encryptedFile.close()


def saveKeys(filepath, key, salt):
    keysFile = open(filepath, 'w')
    keysFile.write(key.hex())
    keysFile.write('\n')
    keysFile.write(salt.hex())
    keysFile.close()
