import base64
import http
import json

from Helpers.SettingsHelper import settings

URL = settings['nordnet']['url']
API_VERSION = settings['nordnet']['api_version']


def send_http_request(conn, method, uri, params, headers):
    """
    Send a HTTP request
    """
    conn.request(method, uri, params, headers)
    r = conn.getresponse()
    response = r.read().decode('utf-8')
    if response == '':
        return ''
    j = json.loads(response)
    return j


def send_auth_http(session_key, method, endpoint_method=None, params=None, headers=None):
    conn = http.client.HTTPSConnection(URL)
    uri = '/next/' + API_VERSION + method
    if headers is None:
        headers = {"Accept": "application/json"}
    if endpoint_method is None:
        endpoint_method = 'GET'
    session_key = session_key + ':' + session_key
    b64_auth = base64.b64encode(bytes(session_key, encoding='utf-8')).decode("utf-8")
    headers['Authorization'] = 'Basic ' + b64_auth
    j = send_http_request(conn, endpoint_method, uri, params, headers)
    return j
