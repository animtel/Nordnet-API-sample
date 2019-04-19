from Helpers.SettingsHelper import settings
from Helpers.ThreadHelper import threading_start
from Services.Auth.LoginService import login_user
from Services.Socket.SocketService import connect_to_feed, receive_message_from_socket, send_cmd_to_socket

SERVICE = settings['nordnet']['service']


def start_listening():
    login_info = login_user()

    # Store NEXT API login response data
    public_feed_hostname = login_info.host
    public_feed_port = login_info.port
    our_session_key = login_info.session_key

    feed_socket = connect_to_feed(public_feed_hostname, public_feed_port)
    threading_start(receive_message_from_socket, (feed_socket,))

    # Login to public feed with our session_key from NEXT API response
    cmd = {"cmd": "login", "args": {"session_key": our_session_key, "service": SERVICE}}
    send_cmd_to_socket(feed_socket, cmd)

    # Subscribe to ERIC B price in public feed
    cmd = {"cmd": "subscribe", "args": {"t": "price", "m": 11, "i": "101"}}
    send_cmd_to_socket(feed_socket, cmd)

    cmd = {"cmd": "subscribe", "args": {"t": "depth", "m": 11, "i": "101"}}
    send_cmd_to_socket(feed_socket, cmd)

    cmd = {"cmd": "subscribe", "args": {"t": "trade", "m": 11, "i": "101"}}
    send_cmd_to_socket(feed_socket, cmd)

    # cmd = {"cmd": "subscribe", "args": {"t": "price", "m": 11, "i": "101"}}
    # send_cmd_to_socket(feed_socket, cmd)
    #
    # cmd = {"cmd": "subscribe", "args": {"t": "price", "m": 11, "i": "101"}}
    # send_cmd_to_socket(feed_socket, cmd)
