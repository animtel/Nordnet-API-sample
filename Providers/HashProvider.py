import base64
import sys
import time
import logging

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from Helpers.SettingsHelper import settings

HASH_FILE_PATH = settings['hash_key_path']


def get_hash(username, password):
    timestamp = int(round(time.time() * 1000))
    timestamp = str(timestamp).encode('ascii')

    username_b64 = base64.b64encode(username.encode('ascii'))
    password_b64 = base64.b64encode(password.encode('ascii'))
    timestamp_b64 = base64.b64encode(timestamp)

    auth_val = username_b64 + b':' + password_b64 + b':' + timestamp_b64
    try:
        public_key_file_handler = open(HASH_FILE_PATH).read()
    except IOError:
        logging.warning("Could not find the following file: " + HASH_FILE_PATH)
        sys.exit()
    rsa_key = RSA.importKey(public_key_file_handler)
    cipher_rsa = PKCS1_v1_5.new(rsa_key)
    encrypted_hash = cipher_rsa.encrypt(auth_val)
    encoded_hash = base64.b64encode(encrypted_hash)

    return encoded_hash
