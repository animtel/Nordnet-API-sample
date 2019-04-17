from flask import Blueprint

from Controllers.Base.BaseController import http_response

user_cotroller = Blueprint('user_cotroller', __name__)


@user_cotroller.route('/login', methods=['GET'])
def get_user():
    from Services.Auth.LoginService import main
    return http_response(main())


@user_cotroller.route('/get', methods=['GET'])
def get_accs():
    from Services.Auth.LoginService import get_accaunts
    return http_response(get_accaunts())


@user_cotroller.route('/test', methods=['GET'])
def get_test():
    from Services.Auth.LoginService import test_main
    test_main()
