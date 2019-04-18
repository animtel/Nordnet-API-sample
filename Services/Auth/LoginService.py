import http
from urllib.parse import urlencode

from Helpers.HttpHelper import send_http_request
from Helpers.SettingsHelper import settings
from Models.Auth.LoginInfoModel import LoginInfoModel
from Providers.HashProvider import get_hash

URL = settings['nordnet']['url']
API_VERSION = settings['nordnet']['api_version']
USERNAME = settings['credentials']['user']
PASSWORD = settings['credentials']['password']
SERVICE = settings['nordnet']['service']


def login_user():
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
    login_info = LoginInfoModel(public_feed_hostname, public_feed_port, our_session_key)
    return login_info
