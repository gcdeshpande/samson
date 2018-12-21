from samson.encoding.openssh.packed_bytes import PackedBytes
from samson.utilities.bytes import Bytes
from samson.encoding.openssh.private_key import PrivateKey
from samson.encoding.openssh.literal import Literal
from samson.padding.incremental_padding import IncrementalPadding
from types import FunctionType

class EdDSAPrivateKey(object):
    """
    OpenSSH encoding for an EdDSA private key.
    """

    def __init__(self, name: str, check_bytes: bytes=None, a: int=None, d: int=None, host: bytes=None):
        """
        Parameters:
            name          (str): Name for bookkeeping purposes.
            check_bytes (bytes): Four random bytes repeated for OpenSSH to check if the decryption worked.
            a             (int): Public int.
            d             (int): Private int.
            host        (bytes): Host the key was generated on.
        """
        self.name = name
        self.check_bytes = check_bytes
        self.a = a
        self.d = d
        self.host = host


    def __repr__(self):
        return f"<EdDSAPrivateKey name={self.name}, a={self.a}, d={self.d}, host={self.host}>"

    def __str__(self):
        return self.__repr__()


    @staticmethod
    def pack(value: object, encryptor: FunctionType=None, padding_size: int=8) -> Bytes:
        """
        Packs a private key into an OpenSSH-compliant encoding.

        Parameters:
            value      (bytes): Value to encode.
            encryptor   (func): (Optional) Function to use as the encryptor.
            padding_size (int): The block size to pad to. Usually 8 unless you're encrypting.
        
        Returns:
            Bytes: Packed bytes.
        """
        check_bytes = Literal('check_bytes', length=8).pack(value.check_bytes)
        encoded = check_bytes + PackedBytes('eddsa-header').pack(b'ssh-ed25519') + PackedBytes('a').pack(value.a) + PackedBytes('d').pack(value.d) + PackedBytes('host').pack(value.host)
    
        padder = IncrementalPadding(padding_size)
        body = padder.pad(encoded)

        if encryptor:
            body = encryptor(body)
        
        body = PackedBytes('private_key').pack(body)

        return body


    @staticmethod
    def unpack(encoded_bytes: bytes, decryptor: FunctionType=None, already_unpacked: bool=False) -> (object, bytes):
        """
        Unpacks bytes into an EdDSAPrivateKey object.

        Parameters:
            encoded_bytes   (bytes): Bytes to be (partially?) decoded.
            already_unpacked (bool): Whether or not to do the initial length-decoding.
        
        Returns:
            (EdDSAPrivateKey, bytes): The decoded object and unused bytes.
        """
        if already_unpacked:
            params, encoded_bytes = Bytes.wrap(encoded_bytes), None
        else:
            params, encoded_bytes = PackedBytes('private_key').unpack(encoded_bytes)
        
        check_bytes, params = PrivateKey.check_decrypt(params, decryptor)

        _header, params = PackedBytes('eddsa-header').unpack(params)
        a, params = PackedBytes('a').unpack(params)
        d, params = PackedBytes('d').unpack(params)
        host, params = PackedBytes('host').unpack(params)

        return EdDSAPrivateKey('private_key', check_bytes=check_bytes, a=a.int(), d=d.int(), host=host), encoded_bytes