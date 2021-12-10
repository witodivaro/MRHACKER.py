import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def deriveKey(key, salt):
    return KDF.PBKDF2(key, salt, dkLen=16, count=1_000_000)


def convertToBytes(el):
    if (isinstance(el, bytes)):
        return el

    return str.encode(el)


def parseEncryption(encryption):
    nonce, ciphertext, tag = [
        bytes.fromhex(x) for x in
        [encryption[:32], encryption[32:-32], encryption[-32:]]
    ]

    return nonce, ciphertext, tag


def encrypt(key, message, salt):
    bytesKey, bytesMessage = [convertToBytes(x) for x in [key, message]]

    derivedKey = deriveKey(bytesKey, salt)
    aes = AES.new(derivedKey, AES.MODE_GCM)
    ciphertext, tag = aes.encrypt_and_digest(bytesMessage)
    encryption = "".join([x.hex() for x in [aes.nonce, ciphertext, tag]])

    return encryption


def decrypt(key, encryption, salt):
    nonce, ciphertext, tag = parseEncryption(encryption)

    bytesKey = convertToBytes(key)
    derivedKey = deriveKey(bytesKey, salt)

    aes = AES.new(derivedKey, AES.MODE_GCM, nonce=nonce)
    plaintext = aes.decrypt_and_verify(ciphertext, tag)

    return plaintext.decode()
