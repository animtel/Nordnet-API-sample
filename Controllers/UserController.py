from flask import Blueprint

from Controllers.Base.BaseController import http_response
from Helpers.ThreadHelper import threading_start
from Services.Auth.LoginService import login_user
from Services.Auth.SubscribeService import start_listen

user_cotroller = Blueprint('user_cotroller', __name__)


@user_cotroller.route('/login', methods=['GET'])
def get_user():
    return http_response(login_user())


@user_cotroller.route('/startListen', methods=['GET'])
def get_test():
    threading_start(start_listen, None)
    return 'Listening started...'
