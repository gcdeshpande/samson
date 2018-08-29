import codecs
from samson.utilities import mod_inv, gen_rand_key, int_to_bytes
import hashlib


class DSA(object):
    def __init__(self):
        self.p = int.from_bytes(codecs.decode(b'800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1', 'hex_codec'), byteorder='big')
        self.q = int.from_bytes(codecs.decode(b'f4f47f05794b256174bba6e9b396a7707e563c5b', 'hex_codec'), byteorder='big')
        self.g = int.from_bytes(codecs.decode(b'5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291', 'hex_codec'), byteorder='big')
        
        self.x = int.from_bytes(gen_rand_key(len(int_to_bytes(self.q))), byteorder='big') % self.q
        self.y = pow(self.g, self.x, self.p)
        
        
    def sign(self, H, message, k=None):
        k = k or max(1, int.from_bytes(gen_rand_key(len(int_to_bytes(self.q))), byteorder='big') % self.q)
        inv_k = mod_inv(k, self.q)
        r = pow(self.g, k, self.p) % self.q
        s = (inv_k * (H(message) + self.x * r)) % self.q
        return (r, s)
    
    
    def verify(self, H, message, sig):
        (r, s) = sig
        w = mod_inv(s, self.q)
        u_1 = (H(message) * w) % self.q
        u_2 = (r * w) % self.q
        v = (pow(self.g, u_1, self.p) * pow(self.y, u_2, self.p) % self.p) % self.q
        return v == r

    
    def derive_k_from_sigs(self, msgA, sigA, msgB, sigB):
        (rA, sA) = sigA
        (rB, sB) = sigB
        assert rA == rB
        
        s = (sA - sB) % self.q
        m = (msgA - msgB) % self.q
        return mod_inv(s, self.q) * m % self.q
    
    
    def derive_x_from_k(self, H, message, k, sig):
        (r, s) = sig
        self.x = ((s * k) - H(message)) * mod_inv(r, self.q) % self.q