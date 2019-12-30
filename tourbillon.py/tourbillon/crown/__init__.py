"""
Crown - 表冠，介接 ETH 進行合約操作
"""

from eth_keyfile import extract_key_from_keyfile
from eth_hash.auto import keccak
from eth_keys import KeyAPI
from eth_keys.datatypes import Signature, PublicKey
from eth_keys.backends import base
from eth_keys.backends import NativeECCBackend


def load_keystore(keystore, passphrase):
    keys = KeyAPI(NativeECCBackend)
    priv = extract_key_from_keyfile(keystore, passphrase)
    return keys.PrivateKey(priv)


def convert_to_hash(timestamp):
    return keccak(timestamp.encode('utf-8'))


def sign_hash(hash, priv):
    keys = KeyAPI(NativeECCBackend)
    sign = keys.ecdsa_sign(hash, priv)
    return sign.to_bytes()


def get_pub_from_priv(priv):
    keys = KeyAPI(NativeECCBackend)
    pub = keys.private_key_to_public_key(priv)
    return pub.to_bytes()


def verify_signature(hash, sig, pub):
    keys = KeyAPI(NativeECCBackend)
    sign = keys.Signature(sig)
    public = keys.PublicKey(pub, base.BaseECCBackend)
    return keys.ecdsa_verify(hash, sign, public)
