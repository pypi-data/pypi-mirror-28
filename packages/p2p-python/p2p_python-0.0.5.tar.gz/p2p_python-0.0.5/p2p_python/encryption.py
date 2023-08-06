#!/user/env python3
# -*- coding: utf-8 -*-

from .utils import str2byte

# For RSA
from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256

# For ECDSA
# from Crypto.Hash import SHA256
from Cryptodome.PublicKey import ECC
from Cryptodome.Signature import DSS

# For AES
from Cryptodome.Cipher import AES
from base64 import b64encode, b64decode
import zlib
import os


class EncryptRSA:
    @staticmethod
    def create_keypair(b=3072):
        rsa = RSA.generate(b, Random.new().read)
        private_pem = rsa.exportKey(format='PEM')
        public_pem = rsa.publickey().exportKey()
        return private_pem.decode(), public_pem.decode()

    @staticmethod
    def sign(private_pem, message, pwd=None):
        key = RSA.importKey(str2byte(private_pem), passphrase=pwd)  # , passphrase='hogehoge')
        h = SHA256.new(message)
        return pkcs1_15.new(key).sign(h)

    @staticmethod
    def verify(public_pem, message, signature, pwd=None):
        key = RSA.importKey(str2byte(public_pem), passphrase=pwd)
        h = SHA256.new(message)
        # Note: When failed verification, raised ValueError
        pkcs1_15.new(key).verify(h, signature)

    @staticmethod
    def encrypt(public_pem, message):
        cipher = PKCS1_OAEP.new(RSA.importKey(str2byte(public_pem)))
        return b64encode(cipher.encrypt(message)).decode()

    @staticmethod
    def decrypt(private_pem, enc):
        msg = b64decode(str2byte(enc))
        cipher = PKCS1_OAEP.new(RSA.importKey(str2byte(private_pem)))
        return cipher.decrypt(msg)


class EncryptECDSA:
    SECP256R1 = 'secp256r1'
    PRIME256V1 = 'prime256v1'

    @staticmethod
    def create_keypair(curve=SECP256R1):
        key = ECC.generate(curve=curve)  # prime256v1, secp256r1
        private_pem = key.export_key(format='PEM')
        public_pem = key.public_key().export_key(format='PEM')
        return private_pem.decode(), public_pem.decode()

    @staticmethod
    def sign(private_pem, message):
        assert type(message) == bytes, 'message should be bytes'
        key = ECC.import_key(str2byte(private_pem))
        h = SHA256.new(message)
        signer = DSS.new(key, 'fips-186-3')
        return signer.sign(h)

    @staticmethod
    def verify(public_pem, message, sign):
        key = ECC.import_key(str2byte(public_pem))
        h = SHA256.new(message)
        verifier = DSS.new(key, 'fips-186-3')
        # Note: When failed verification, raised ValueError
        verifier.verify(h, sign)


class AESCipher:
    @staticmethod
    def create_key():
        return b64encode(os.urandom(32)).decode()

    @staticmethod
    def is_aes_key(key):
        try:
            return len(b64decode(key.encode())) == 32
        except:
            return False

    @staticmethod
    def encrypt(key, raw, z=True):
        assert type(raw) == bytes, "input data is bytes"
        if z:
            raw = zlib.compress(raw)
        key = b64decode(str2byte(key))
        raw = AESCipher._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    @staticmethod
    def decrypt(key, enc, z=True):
        assert type(enc) == bytes, 'Encrypt data is bytes'
        key = b64decode(str2byte(key))
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        raw = AESCipher._unpad(cipher.decrypt(enc[AES.block_size:]))
        if len(raw) == 0:
            raise Exception("not correct pwd")
        elif z:
            return zlib.decompress(raw)
        else:
            return raw

    @staticmethod
    def _pad(s):
        pad = 32 - len(s) % 32
        add = 32 - len(s) % 32
        return s + add * pad.to_bytes(1, 'big')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

