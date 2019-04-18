import json


def send_http_request(conn, method, uri, params, headers):
    """
    Send a HTTP request
    """
    conn.request(method, uri, params, headers)
    r = conn.getresponse()
    response = r.read().decode('utf-8')
    j = json.loads(response)
    return j
