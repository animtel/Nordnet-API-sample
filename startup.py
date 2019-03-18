from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine

from Controllers.Base.BaseController import BaseController


class Startup:
    def __init__(self):
        self.__db_connect = create_engine('sqlite:///chinook.db')
        self.__app = Flask(__name__)
        self.__app.config["DEBUG"] = True
        self.__api = Api(self.__app)

    def app_init(self):
        self.__app.run(port='5002')

    @property
    def db(self):
        return self.__db_connect

    @property
    def app(self):
        return self.__app


app_start = Startup()
db_connect = app_start.db
app = app_start.app

bsController = BaseController(db_connect, app)

app_start.app_init()
