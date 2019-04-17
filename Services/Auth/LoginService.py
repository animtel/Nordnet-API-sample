import time
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import http.client
import json
from urllib.parse import urlencode, quote_plus

from Factories.UserFactory import CreateUserForAuth
from Helpers.SettingsHelper import settings

SERVICE = settings['nordnet']['service']
URL = settings['nordnet']['url']
API_VERSION = settings['nordnet']['api_version']


def print_json(j, prefix=''):
    for key, value in j.items():
        if isinstance(value, dict):
            print('%s%s' % (prefix, key))
            print_json(value, prefix + '  ')
        else:
            print('%s%s:%s' % (prefix, key, value))


def get_hash(username, password):
    timestamp = int(round(time.time() * 1000))
    timestamp = str(timestamp).encode('ascii')

    username_b64 = base64.b64encode(username.encode('ascii'))
    password_b64 = base64.b64encode(password.encode('ascii'))
    timestamp_b64 = base64.b64encode(timestamp)

    auth_val = username_b64 + b':' + password_b64 + b':' + timestamp_b64
    rsa_key = RSA.importKey(open('Services/Auth/NEXTAPI_TEST_public.pem').read())
    cipher_rsa = PKCS1_v1_5.new(rsa_key)
    encrypted_hash = cipher_rsa.encrypt(auth_val)
    encoded_hash = base64.b64encode(encrypted_hash)

    print(auth_val, encoded_hash)
    return encoded_hash


def main():
    user = CreateUserForAuth()
    auth_hash = get_hash(user.name, user.password)

    headers = {"Accept": "application/json"}
    conn = http.client.HTTPSConnection(URL)

    # GET server status
    conn.request('GET', '/next/' + API_VERSION + '/', '', headers)
    r = conn.getresponse()
    response = r.read().decode('utf-8')
    j = json.loads(response)
    print_json(j)

    # POST login
    params = urlencode({'service': 'NEXTAPI', 'auth': auth_hash})
    conn.request('POST', '/next/' + API_VERSION + '/login', params, headers)
    r = conn.getresponse()
    response = r.read().decode('utf-8')
    j = json.loads(response)
    print_json(j)
    return j
