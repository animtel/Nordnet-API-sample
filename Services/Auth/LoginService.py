import socket
import ssl
import sys
import time
import base64
from multiprocessing import Process
from threading import Thread

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
    try:
        public_key_file_handler = open('Services/Auth/NEXTAPI_TEST_public.pem').read()
    except IOError:
        print("Could not find the following file: ",
              "\"", 'Services/Auth/NEXTAPI_TEST_public.pem', "\"", sep="")
        sys.exit()
    rsa_key = RSA.importKey(public_key_file_handler)
    cipher_rsa = PKCS1_v1_5.new(rsa_key)
    encrypted_hash = cipher_rsa.encrypt(auth_val)
    encoded_hash = base64.b64encode(encrypted_hash)

    return encoded_hash


def send_cmd_to_socket(socket, cmd):
    """
    Send commands to the feed through the socket
    """
    socket.send(bytes(json.dumps(cmd) + '\n', 'utf-8'))
    print("<< Sending cmd to feed: " + str(cmd))


def connect_to_feed(public_feed_hostname, public_feed_port):
    """
    Connect to the feed and get back a TCP socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if public_feed_port == 443:
        s = ssl.wrap_socket(s)
    s.connect((public_feed_hostname, public_feed_port))
    return s


def send_http_request(conn, method, uri, params, headers):
    """
    Send a HTTP request
    """
    conn.request(method, uri, params, headers)
    r = conn.getresponse()
    response = r.read().decode('utf-8')
    j = json.loads(response)
    return j


def try_parse_into_json(string):
    """
    Try parsing the string into JSON objects. Return the unparsable
    parts as buffer
    """
    json_strings = string.split('\n')

    for i in range(0, len(json_strings)):
        try:
            json_data = json.loads(json_strings[i])
        except:
            ## If this part cannot be parsed into JSON, It's probably not
            ## complete. Stop it right here. Merge the rest of list and
            ## return it, parse it next time
            return ''.join(json_strings[i:])

    ## If all JSONs are successfully parsed, we return an empty buffer
    return ''


def do_receive_from_socket(socket, last_buffer):
    """
    Receive data from the socket, and try to parse it into JSON. Return
    the unparsable parts as buffer
    """
    # Consume message (price data or heartbeat) from public feed
    # > Note that a full message with all the JSON objects ends with a
    # > newline symbol "\n". As such you need to listen and read from
    # > the buffer until a full message has been transferred
    time.sleep(0.01)
    new_data = socket.recv(1024).decode('utf-8')

    string = last_buffer + new_data
    if string != '':
        new_buffer = try_parse_into_json(string)
        return new_buffer

    return ''


def receive_message_from_socket(socket):
    """
    Receive data from the socket and parse it
    """
    buffer = ''
    while True:
        buffer = do_receive_from_socket(socket, buffer)


def threading_start(func, args):
    proc = Thread(target=func, args=args)
    proc.start()


def test_main():
    USERNAME = 'Antsybor'
    PASSWORD = 'EkTCuSJzN4hHZINEXnsu'
    auth_hash = get_hash(USERNAME, PASSWORD)

    headers = {"Accept": "application/json"}
    conn = http.client.HTTPSConnection(URL)

    # POST login to NEXT API. Check NEXT API documentation page to verify the path
    uri = '/next/' + API_VERSION + '/login'
    params = urlencode({'service': SERVICE, 'auth': auth_hash})
    j = send_http_request(conn, 'POST', uri, params, headers)

    # Store NEXT API login response data
    public_feed_hostname = j["public_feed"]["hostname"]
    public_feed_port = j["public_feed"]["port"]
    our_session_key = j["session_key"]

    feed_socket = connect_to_feed(public_feed_hostname, public_feed_port)
    threading_start(receive_message_from_socket, (feed_socket,))

    # Login to public feed with our session_key from NEXT API response
    cmd = {"cmd": "login", "args": {"session_key": our_session_key, "service": "NEXTAPI"}}
    send_cmd_to_socket(feed_socket, cmd)

    # Subscribe to ERIC B price in public feed
    cmd = {"cmd": "subscribe", "args": {"t": "price", "m": 11, "i": "101"}}
    send_cmd_to_socket(feed_socket, cmd)

    console_input = ""
    while console_input != "exit":
        console_input = input()
        try:
            cmd = json.loads(console_input)
            send_cmd_to_socket(feed_socket, cmd)
        except Exception as e:
            print(e)

    feed_socket.shutdown(socket.SHUT_RDWR)
    feed_socket.close()
    sys.exit(0)


def main():
    user = CreateUserForAuth()
    auth_hash = get_hash(user.name, user.password)
    print(auth_hash)

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


def get_accaunts():
    # session_key
    authJson = main()["session_key"]
    print(authJson)
    headers = {"Accept": "application/json", "Authorization": authJson}
    conn = http.client.HTTPSConnection(URL)
    params = urlencode({'service': 'NEXTAPI', 'Authorization': authJson})
    conn.request('GET', '/next/' + API_VERSION + '/accounts', '', headers)
    r = conn.getresponse()
    response = r.read().decode('utf-8')
    j = json.loads(response)
    print_json(j)
    return j
