from flask import Blueprint

from Controllers.Base.BaseController import http_response
from Helpers.HttpHelper import send_auth_http
from Helpers.MappingHelper import to_dynamic, update_exist_props
from Helpers.ThreadHelper import threading_start
from Repositories.PriceRepository import import_price_from_socket
from Services.Auth.LoginService import login_user
from Services.Auth.SubscribeService import start_listening

user_cotroller = Blueprint('user_cotroller', __name__)


@user_cotroller.route('/accounts', methods=['GET'])
def get_accaounts():
    user_info = login_user()
    j = send_auth_http(user_info.session_key, '/accounts')
    return http_response(j)


@user_cotroller.route('/startListen', methods=['GET'])
def start_listen():
    threading_start(start_listening, (import_price_from_socket,))
    return 'Listening started...'


def iport_test(json_string):
    fullJson = '{"type":"price","data":{"i":"101","m":11,"trade_timestamp":1556611255666,"tick_timestamp":1556619399552,"bid":90.00,"bid_volume":167,"ask":0.0000,"ask_volume":0,"close":94.66,"high":94.00,"last":94.00,"last_volume":100,"low":94.00,"open":94.00,"vwap":94.00,"turnover":9400.00,"turnover_volume":100}}'
    notFullJson = '{"type":"price","data":{"i":"101","m":11,"trade_timestamp":1556630296604,"tick_timestamp":1556630296605,"ep":null,"paired":null,"imbalance":null}}'
    fullObj = to_dynamic(fullJson).data
    notFullObj = to_dynamic(notFullJson).data

    test = update_exist_props(fullObj, notFullObj)

    print(test)
