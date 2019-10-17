
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256

KEY_SIZE = 2048

def generate_key(keysize=KEY_SIZE):
    """Generate a RSA key pair

    Keyword Arguments:
        keysize {int} -- Key (default: {KEY_SIZE})

    Returns:
        bytes -- Secret key
        bytes -- Public key
    """
    key = RSA.generate(keysize)
    public_key = key.publickey().exportKey()
    secret_key = key.exportKey(passphrase=None)
    return secret_key, public_key


def signature(secret_key, data):
    """Generate digital signature

    Arguments:
        secret_key {bytes} -- RSA secret key
        data {bytes} -- Data

    Returns:
        bytes -- signature
    """
    rsakey = RSA.importKey(secret_key, passphrase=None)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data)
    signature = signer.sign(digest)

    return signature

def verify(public_key, signature, data):
    """Verify data from signature

    Arguments:
        public_key {bytes} -- RSA Public key
        signature {bytes} -- Signature
        data {bytes} -- Data

    Returns:
        int -- 0: Ok, 1: Fail
    """

    rsakey = RSA.importKey(public_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data)

    if signer.verify(digest, signature):
        return 0

    return -1
