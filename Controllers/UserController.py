from urllib.parse import urlencode

from flask import Blueprint, request

from Controllers.Base.BaseController import http_response
from Helpers.HttpHelper import send_auth_http
from Helpers.StringHelper import get_json_from_request_data
from Helpers.ThreadHelper import threading_start
from Repositories.PriceRepository import import_price_from_socket
from Services.Auth.LoginService import login_user
from Services.Auth.SubscribeService import start_listening

user_cotroller = Blueprint('user_cotroller', __name__)


@user_cotroller.route('/accounts', methods=['GET'])
def get_accaounts():
    user_info = login_user()
    result = send_auth_http(user_info.session_key, '/accounts')
    return http_response(result)


@user_cotroller.route('/getorderstate/<orderid>', methods=['GET'])
def get_order_state(orderid):
    user_info = login_user()
    accounts = send_auth_http(user_info.session_key, '/accounts')
    acc_number = accounts[0]["accno"]
    endoint = '/accounts/' + str(acc_number) + '/orders'
    orders = send_auth_http(user_info.session_key, endoint)
    temp_order = list(filter(lambda x: str(x["order_id"]) == str(orderid), orders))[0]
    return temp_order["order_state"]


@user_cotroller.route('/deleteoder/<orderid>', methods=['GET'])
def delete_order(orderid):
    user_info = login_user()
    accounts = send_auth_http(user_info.session_key, '/accounts')
    acc_number = accounts[0]["accno"]
    endoint = '/accounts/' + str(acc_number) + '/orders/' + orderid
    respond = send_auth_http(user_info.session_key, endoint, 'DELETE')
    return http_response(respond)


@user_cotroller.route('/orders', methods=['GET'])
def get_orders():
    user_info = login_user()
    accounts = send_auth_http(user_info.session_key, '/accounts')
    acc_number = accounts[0]["accno"]
    endoint = '/accounts/' + str(acc_number) + '/orders'
    result = send_auth_http(user_info.session_key, endoint)
    return http_response(result)


@user_cotroller.route('/createOrder', methods=['POST'])
def create_order():
    data = get_json_from_request_data(request.data)
    acc_number = data['acc_number']  # The account number of the account to use
    identifier = data['identifier']  # Nordnet tradable identifier
    market_id = data['market_id']  # Nordnet market identifier
    price = data['price']  # The price limit of the order
    currency = data['currency']  # The currency that the instrument is traded in
    volume = data['volume']  # The volume of the order
    side = data['side']  # BUY / SELL
    order_type = data[
        'order_type']  # NORMAL is the default if order_type is left out, when using NORMAL the system guess the
    # order type based on used parameters. In order to get better parameter validation and to ensure that the order
    # type is the desired the client should not use NORMAL, please user the intended order type. NORMAL will be
    # deprecated in future versions
    user_info = login_user()
    endoint = '/accounts/' + str(acc_number) + '/orders'
    endpoint_method = 'POST'
    post_data = urlencode({
        "identifier": int(identifier),
        "market_id": int(market_id),
        "price": float(price),
        "currency": currency,
        "volume": int(volume),
        "side": side,
        "order_type": order_type
    })
    result = send_auth_http(user_info.session_key, endoint, endpoint_method, params=post_data)
    return http_response(result)


@user_cotroller.route('/startListenPrices', methods=['GET'])
def start_listen():
    threading_start(start_listening, (import_price_from_socket,))
    return 'Listening started...'
