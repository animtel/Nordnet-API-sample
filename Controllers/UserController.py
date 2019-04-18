from flask import Blueprint

from Controllers.Base.BaseController import http_response
from Helpers.HttpHelper import send_auth_http
from Helpers.ThreadHelper import threading_start
from Services.Auth.LoginService import login_user
from Services.Auth.SubscribeService import start_listen

user_cotroller = Blueprint('user_cotroller', __name__)


@user_cotroller.route('/accounts', methods=['GET'])
def get_accaounts():
    user_info = login_user()
    j = send_auth_http(user_info.session_key, '/accounts')
    return http_response(j)

@user_cotroller.route('/startListen', methods=['GET'])
def start_listen():
    threading_start(start_listen, None)
    return 'Listening started...'
