from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException

from Controllers.UserController import user_cotroller

HOST = '0.0.0.0'
PORT = '80'
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://' + HOST + ':' + PORT + '/static/swagger.json'  # Our API url (can of course be a local resource)


# initdb()


class Startup:
    def __init__(self):
        self.__app = Flask(__name__)
        self.__api = Api(self.__app)
        self.__app.config["DEBUG"] = True

    # logging.basicConfig(filename='logs.log', level=logging.DEBUG)

    def app_init(self):
        if PORT != '':
            self.__app.run(HOST, PORT)
        else:
            self.__app.run(HOST)

    @property
    def app(self):
        return self.__app

    @property
    def api(self):
        return self.__api


app_start = Startup()
app = app_start.app
api = app_start.api

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "NordnetAPI"})
# cotroller registration:
app.register_error_handler(HTTPException, lambda e: (str(e), e.code))
app.register_blueprint(user_cotroller, url_prefix='/user')
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# app start:
if __name__ == '__main__':
    app_start.app_init()
