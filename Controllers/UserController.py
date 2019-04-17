from flask import Blueprint

from Controllers.Base.BaseController import http_response

user_cotroller = Blueprint('user_cotroller', __name__)


@user_cotroller.route('/login', methods=['GET'])
def get_user():
    from Services.Auth.LoginService import main
    return http_response(main())
