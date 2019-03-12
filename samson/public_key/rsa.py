from samson.utilities.math import gcd, lcm, mod_inv, find_prime
from samson.core.encryption_alg import EncryptionAlg

from samson.encoding.openssh.openssh_rsa_private_key import OpenSSHRSAPrivateKey
from samson.encoding.openssh.openssh_rsa_public_key import OpenSSHRSAPublicKey
from samson.encoding.openssh.ssh2_rsa_public_key import SSH2RSAPublicKey
from samson.encoding.jwk.jwk_rsa_public_key import JWKRSAPublicKey
from samson.encoding.jwk.jwk_rsa_private_key import JWKRSAPrivateKey
from samson.encoding.pkcs1.pkcs1_rsa_private_key import PKCS1RSAPrivateKey
from samson.encoding.pkcs8.pkcs8_rsa_private_key import PKCS8RSAPrivateKey
from samson.encoding.pkcs1.pkcs1_rsa_public_key import PKCS1RSAPublicKey
from samson.encoding.x509.x509_rsa_certificate import X509RSACertificate
from samson.encoding.x509.x509_rsa_public_key import X509RSAPublicKey
from samson.encoding.general import PKIEncoding

from samson.encoding.pem import pem_encode, pem_decode
from samson.utilities.bytes import Bytes
from samson.core.encodable_pki import EncodablePKI
import random

class RSA(EncryptionAlg, EncodablePKI):
    """
    Rivest-Shamir-Adleman public key cryptosystem
    """

    PRIV_ENCODINGS = {
        PKIEncoding.JWK: JWKRSAPrivateKey,
        PKIEncoding.OpenSSH: OpenSSHRSAPrivateKey,
        PKIEncoding.PKCS1: PKCS1RSAPrivateKey,
        PKIEncoding.PKCS8: PKCS8RSAPrivateKey
    }


    PUB_ENCODINGS = {
        PKIEncoding.JWK: JWKRSAPublicKey,
        PKIEncoding.OpenSSH: OpenSSHRSAPublicKey,
        PKIEncoding.SSH2: SSH2RSAPublicKey,
        PKIEncoding.X509_CERT: X509RSACertificate,
        PKIEncoding.X509: X509RSAPublicKey,
        PKIEncoding.PKCS1: PKCS1RSAPublicKey
    }

    def __init__(self, bits: int, p: int=None, q: int=None, e: int=65537):
        """
        Parameters:
            bits (int): Number of bits for strength and capacity.
            p    (int): Secret prime modulus.
            q    (int): Secret prime modulus.
            e    (int): Public exponent.
        """
        self.e = e
        phi = 0

        if p and q:
            phi = lcm(p - 1, q - 1)
            self.n = p * q

            if gcd(self.e, phi) != 1:
                raise Exception("Invalid 'p' and 'q': GCD(e, phi) != 1")

            bits = p.bit_length() + q.bit_length()
        else:
            next_p = p
            next_q = q
            while gcd(self.e, phi) != 1 or next_p == next_q:
                if not p:
                    next_p = find_prime(bits // 2)

                if not q:
                    next_q = find_prime(bits // 2)

                phi = lcm(next_p - 1, next_q - 1)

            p = next_p
            q = next_q
            self.n = p * q

        self.p = p
        self.q = q

        self.bits = bits

        self.phi = phi
        self.d = mod_inv(self.e, phi)
        self.alt_d = mod_inv(self.e, (self.p - 1) * (self.q - 1))

        self.dP = self.d % (self.p-1)
        self.dQ = self.d % (self.q-1)
        self.Qi = mod_inv(self.q, self.p)

        self.pub = (self.e, self.n)
        self.priv = (self.d, self.n)



    def __repr__(self):
        return f"<RSA: bits={self.bits}, p={self.p}, q={self.q}, e={self.e}, n={self.n}, phi={self.phi}, d={self.d}, alt_d={self.alt_d}>"

    def __str__(self):
        return self.__repr__()



    def encrypt(self, plaintext: bytes) -> int:
        """
        Encrypts `plaintext`.

        Parameters:
            plaintext (bytes): Plaintext.
        
        Returns:
            int: Ciphertext.
        """
        m = Bytes.wrap(plaintext).int()
        return pow(m, self.e, self.n)



    def decrypt(self, ciphertext: int) -> Bytes:
        """
        Decrypts `ciphertext` back into plaintext.

        Parameters:
            ciphertext (int): Ciphertext.
        
        Returns:
            Bytes: Decrypted plaintext.
        """
        plaintext = pow(ciphertext, self.d, self.n)
        return Bytes(plaintext, 'big')



    # def export_private_key(self, encode_pem: bool=True, encoding: PKIEncoding=PKIEncoding.PKCS1, marker: str=None, encryption: str=None, passphrase: bytes=None, iv: bytes=None) -> bytes:
    #     """
    #     Exports the full RSA instance into encoded bytes.
    #     See https://tools.ietf.org/html/rfc2313#section-7.2.

    #     Parameters:
    #         encode_pem      (bool): Whether or not to PEM-encode as well.
    #         encoding (PKIEncoding): Encoding scheme to use. Currently supports 'PKCS1', 'PKCS8', 'JWK', and 'OpenSSH'.
    #         marker           (str): Marker to use in PEM formatting (if applicable).
    #         encryption       (str): (Optional) RFC1423 encryption algorithm (e.g. 'DES-EDE3-CBC').
    #         passphrase     (bytes): (Optional) Passphrase to encrypt DER-bytes (if applicable).
    #         iv             (bytes): (Optional) IV to use for CBC encryption.
        
    #     Returns:
    #         bytes: Bytes-encoded RSA instance.
    #     """
    #     if encoding == PKIEncoding.PKCS1:
    #         encoded = PKCS1RSAPrivateKey.encode(self)

    #         if encode_pem:
    #             encoded = pem_encode(encoded, marker or PKCS1RSAPrivateKey.DEFAULT_MARKER, encryption=encryption, passphrase=passphrase, iv=iv)

    #     elif encoding == PKIEncoding.PKCS8:
    #         encoded = PKCS8RSAPrivateKey.encode(self)

    #         if encode_pem:
    #             encoded = pem_encode(encoded, marker or PKCS8RSAPrivateKey.DEFAULT_MARKER, encryption=encryption, passphrase=passphrase, iv=iv)

    #     elif encoding == PKIEncoding.OpenSSH:
    #         encoded = OpenSSHRSAPrivateKey.encode(self, encode_pem, marker, encryption, iv, passphrase)

    #     elif encoding == PKIEncoding.JWK:
    #         encoded = JWKRSAPrivateKey.encode(self)

    #     else:
    #         raise ValueError(f'Unsupported encoding "{encoding}"')

    #     return encoded



    # def export_public_key(self, encode_pem: bool=None, encoding: PKIEncoding=PKIEncoding.PKCS1, marker: str=None) -> bytes:
    #     """
    #     Exports the only the public parameters of the RSA instance into encoded bytes.
    #     See https://tools.ietf.org/html/rfc2313#section-7.2.

    #     Parameters:
    #         encode_pem      (bool): Whether or not to PEM-encode as well.
    #         encoding (PKIEncoding): Encoding scheme to use. Currently supports 'PKCS1', 'X509', 'JWK', 'OpenSSH', and 'SSH2'.
    #         marker           (str): Marker to use in PEM formatting (if applicable).

    #     Returns:
    #         bytes: Encoding of RSA instance.
    #     """
    #     use_rfc_4716 = False

    #     if encoding == PKIEncoding.PKCS1:
    #         encoded = PKCS1RSAPublicKey.encode(self)
    #         default_marker = PKCS1RSAPublicKey.DEFAULT_MARKER
    #         default_pem = PKCS1RSAPublicKey.DEFAULT_PEM

    #     elif encoding == PKIEncoding.X509:
    #         encoded = X509RSAPublicKey.encode(self)
    #         default_marker = X509RSAPublicKey.DEFAULT_MARKER
    #         default_pem = X509RSAPublicKey.DEFAULT_PEM

    #     elif encoding == PKIEncoding.X509_CERT:
    #         encoded = X509RSACertificate.encode(self)
    #         default_marker = X509RSACertificate.DEFAULT_MARKER
    #         default_pem = X509RSACertificate.DEFAULT_PEM

    #     elif encoding== PKIEncoding.JWK:
    #         encoded = JWKRSAPublicKey.encode(self)
    #         default_pem = JWKRSAPublicKey.DEFAULT_PEM

    #     elif encoding == PKIEncoding.OpenSSH:
    #         encoded = OpenSSHRSAPublicKey.encode(self)
    #         default_marker = OpenSSHRSAPublicKey.DEFAULT_MARKER
    #         default_pem = OpenSSHRSAPublicKey.DEFAULT_PEM

    #     elif encoding == PKIEncoding.SSH2:
    #         encoded = SSH2RSAPublicKey.encode(self)
    #         default_marker = SSH2RSAPublicKey.DEFAULT_MARKER
    #         default_pem = SSH2RSAPublicKey.DEFAULT_PEM
    #         use_rfc_4716 = SSH2RSAPublicKey.USE_RFC_4716

    #     else:
    #         raise ValueError(f'Unsupported encoding "{encoding}"')


    #     if (encode_pem is None and default_pem) or encode_pem:
    #         encoded = pem_encode(encoded, marker or default_marker, use_rfc_4716=use_rfc_4716)

    #     return encoded



    # @staticmethod
    # def import_key(buffer: bytes, passphrase: bytes=None):
    #     """
    #     Builds an RSA instance from DER and/or PEM-encoded bytes.

    #     Parameters:
    #         buffer     (bytes): DER and/or PEM-encoded bytes.
    #         passphrase (bytes): Passphrase to decrypt DER-bytes (if applicable).
        
    #     Returns:
    #         RSA: RSA instance.
    #     """
    #     if buffer.startswith(b'----'):
    #         buffer = pem_decode(buffer, passphrase)

        
    #     # JWK
    #     if JWKRSAPrivateKey.check(buffer):
    #         rsa = JWKRSAPrivateKey.decode(buffer)

    #     elif JWKRSAPublicKey.check(buffer):
    #         rsa = JWKRSAPublicKey.decode(buffer)

    #     # SSH
    #     elif OpenSSHRSAPrivateKey.check(buffer, passphrase):
    #         rsa = OpenSSHRSAPrivateKey.decode(buffer, passphrase)

    #     elif OpenSSHRSAPublicKey.check(buffer):
    #         rsa = OpenSSHRSAPublicKey.decode(buffer)

    #     elif SSH2RSAPublicKey.check(buffer):
    #         rsa = SSH2RSAPublicKey.decode(buffer)

    #     # X.509
    #     elif X509RSACertificate.check(buffer):
    #         rsa = X509RSACertificate.decode(buffer)

    #     elif X509RSAPublicKey.check(buffer):
    #         rsa = X509RSAPublicKey.decode(buffer)

    #     # PKCS8
    #     elif PKCS8RSAPrivateKey.check(buffer):
    #         rsa = PKCS8RSAPrivateKey.decode(buffer)

    #     # PKCS#1
    #     elif PKCS1RSAPrivateKey.check(buffer):
    #         rsa = PKCS1RSAPrivateKey.decode(buffer)

    #     elif PKCS1RSAPublicKey.check(buffer):
    #         rsa = PKCS1RSAPublicKey.decode(buffer)
    #     else:
    #         raise ValueError("Unable to parse provided RSA key.")

    #     rsa.bits = rsa.n.bit_length()
    #     return rsa




    @staticmethod
    def factorize_from_shared_p(n1: int, n2: int, e: int):
        """
        Factorizes the moduli of two instances that share a common secret prime. See `Batch GCD`.

        Parameters:
            n1 (int): Modulus of the first instance.
            n2 (int): Modulus of the second instance.
            e  (int): Public exponent.
        
        Returns:
            (RSA, RSA): Both cracked RSA instances.
        """
        assert n1 != n2

        # Find shared `p`
        p = gcd(n1, n2)

        q1 = n1 // p
        q2 = n2 // p

        return (RSA(0, p=p, q=q1, e=e), RSA(0, p=p, q=q2, e=e))


    @staticmethod
    def factorize_from_faulty_crt(message: int, faulty_sig: int, e: int, n: int):
        """
        Factorize the secret primes from a faulty signature produced with CRT-optimized RSA.

        Parameters:
            message    (int): Message.
            faulty_sig (int): Faulty signature of `message`.
            e          (int): Public exponent.
            n          (int): Modulus.
        
        Returns:
            RSA: Cracked RSA instance.
        """
        q = gcd(pow(faulty_sig, e, n) - message, n)
        p = n // q

        return RSA(0, p=p, q=q, e=e)


    @staticmethod
    def factorize_from_d(d: int, e: int, n: int):
        """
        Factorizes the secret primes from the private key `d`.

        Parameters:
            d (int): Private key.
            e (int): Public exponent.
            n (int): Modulus.
        
        Returns:
            RSA: Full RSA instance.
        """
        k = d*e - 1
        p = None
        q = None

        while not p:
            g = random.randint(2, n - 1)
            t = k

            while t % 2 == 0:
                t = t // 2
                x = pow(g, t, n)

                if x > 1 and gcd(x - 1, n) > 1:
                    p = gcd(x - 1, n)
                    q = n // p
                    break

        return RSA(0, p=p, q=q, e=e)
