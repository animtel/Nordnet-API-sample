import logging

from flask import Flask

from Controllers.EmployeesController import employees_cotroller
from Controllers.UserController import user_cotroller

HOST = 'localhost'
PORT = '5002'


class Startup:
    def __init__(self):
        self.__app = Flask(__name__)
        self.__app.config["DEBUG"] = True
        logging.basicConfig(filename='logs.log', level=logging.DEBUG)

    def app_init(self):
        self.__app.run(HOST, PORT)

    @property
    def app(self):
        return self.__app

app_start = Startup()
app = app_start.app
logging.info('App Started')

# cotroller registration:
app.register_blueprint(employees_cotroller, url_prefix='/employees')
app.register_blueprint(user_cotroller, url_prefix='/user')

# app start:
app_start.app_init()
