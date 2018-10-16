from samson.utilities.manipulation import get_blocks
from samson.utilities.padding import pkcs7_pad, pkcs7_unpad
from samson.utilities.bytes import Bytes


class CBC(object):
    def __init__(self, encryptor, decryptor, iv, block_size):
        self.encryptor = encryptor
        self.decryptor = decryptor
        self.iv = iv
        self.block_size = block_size


    def __repr__(self):
        return f"<CBC: encryptor={self.encryptor}, decryptor={self.decryptor}, iv={self.iv}, block_size={self.block_size}>"


    def __str__(self):
        return self.__repr__()


    def encrypt(self, plaintext, pad=True):
        plaintext = Bytes.wrap(plaintext)

        if pad:
            plaintext = pkcs7_pad(plaintext, self.block_size)

        if len(plaintext) % self.block_size != 0:
            raise Exception("Plaintext is not a multiple of the block size")

        ciphertext = Bytes(b'')
        last_block = self.iv

        for block in get_blocks(plaintext, self.block_size):
            enc_block = self.encryptor(bytes(last_block ^ block))
            ciphertext += enc_block
            last_block = enc_block
        
        return ciphertext


    def decrypt(self, ciphertext, unpad=True):
        plaintext = b''

        if len(ciphertext) % self.block_size != 0:
            raise Exception("Ciphertext is not a multiple of the block size")

        last_block = self.iv
        for block in get_blocks(ciphertext, self.block_size):
            enc_block = last_block ^ Bytes.wrap(self.decryptor(block))
            plaintext += enc_block
            last_block = block

        if unpad: plaintext = pkcs7_unpad(plaintext, self.block_size)
        return plaintext
