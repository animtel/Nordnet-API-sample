import json
import logging
import socket
import ssl
import time

from Helpers.MappingHelper import to_dynamic
from Helpers.StringHelper import try_parse_into_json


def send_cmd_to_socket(socket, cmd):
    """
    Send commands to the feed through the socket
    """
    socket.send(bytes(json.dumps(cmd) + '\n', 'utf-8'))
    logging.info("<< Sending cmd to feed: " + str(cmd))


def connect_to_feed(public_feed_hostname, public_feed_port):
    """
    Connect to the feed and get back a TCP socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if public_feed_port == 443:
        s = ssl.wrap_socket(s)
    s.connect((public_feed_hostname, public_feed_port))
    return s


def do_receive_from_socket(socket, importdb_func, last_buffer):
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
    importdb_func(new_data)
    # string = last_buffer + new_data
    # if string != '':
    #     new_buffer = try_parse_into_json(string)
    #     return new_buffer
    #
    # return ''


def receive_message_from_socket(socket, importdb_func):
    """
    Receive data from the socket and parse it
    """
    buffer = ''
    while True:
        buffer = do_receive_from_socket(socket, importdb_func, buffer)
