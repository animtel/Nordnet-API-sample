from urllib.parse import urlencode

from flask import Blueprint

from Controllers.Base.BaseController import http_response
from Helpers.HttpHelper import send_auth_http
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


@user_cotroller.route('/orders', methods=['GET'])
def get_orders():
    user_info = login_user()
    accounts = send_auth_http(user_info.session_key, '/accounts')
    acc_number = accounts[0]["accno"]
    endoint = '/accounts/' + str(acc_number) + '/orders'
    result = send_auth_http(user_info.session_key, endoint)
    return http_response(result)


@user_cotroller.route('/orders', methods=['POST'])
def get_accaounts():
    user_info = login_user()
    accounts = send_auth_http(user_info.session_key, '/accounts')
    markets = send_auth_http(user_info.session_key, '/markets')
    acc_number = accounts[0]["accno"]
    market_id = markets[0]["market_id"]
    endoint = '/accounts/' + str(acc_number) + '/orders'
    endpoint_method = 'POST'
    test = urlencode({"accno": acc_number, "market_id": market_id})
    # result = send_auth_http(user_info.session_key, endoint, endpoint_method)
    return ''
    return http_response(result)


@user_cotroller.route('/startListen', methods=['GET'])
def start_listen():
    threading_start(start_listening, (import_price_from_socket,))
    return 'Listening started...'
