from tourbillon import crown, calibre


def test_load_keystore():
    passphrase = b'!QAZ 2wsx 3edc'
    keystore = 'config/owner_keystore'
    priv = crown.load_keystore(keystore, passphrase)
    assert priv is not None
    assert len(priv) == 64


def test_convert_timestamp_to_hash():
    timestamp = calibre.get_now()
    hash = crown.convert_to_hash(timestamp)
    assert hash is not None
    assert type(hash) is bytes
    assert len(hash) == 32


def test_get_pub_from_priv():
    passphrase = b'!QAZ 2wsx 3edc'
    keystore = 'config/owner_keystore'
    priv = crown.load_keystore(keystore, passphrase)
    pub = crown.get_pub_from_priv(priv)
    assert pub is not None
    assert len(pub) == 64


def test_sign_hash():
    passphrase = b'!QAZ 2wsx 3edc'
    keystore = 'config/owner_keystore'
    priv = crown.load_keystore(keystore, passphrase)
    timestamp = calibre.get_now()
    hash = crown.convert_to_hash(timestamp)
    sign = crown.sign_hash(hash, priv)
    assert sign is not None
    assert len(sign) == 65


def test_verify_signature():
    passphrase = b'!QAZ 2wsx 3edc'
    keystore = 'config/owner_keystore'
    priv = crown.load_keystore(keystore, passphrase)
    pub = crown.get_pub_from_priv(priv)
    timestamp = calibre.get_now()
    hash = crown.convert_to_hash(timestamp)
    sign = crown.sign_hash(hash, priv)
    assert crown.verify_signature(hash, sign, pub)
