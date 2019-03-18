from flask_restful import Resource, Api
from flask import Flask, request, jsonify

from Helpers import route


class BaseController(Resource):
    flaskApp = None

    def __init__(self, db_connect, app):
        self.__db_conn = db_connect
        self.__app = app
        flaskApp = app

    @property
    def db(self):
        return self.__db_conn

    @property
    def app(self):
        return self.__app

    def http_response(self, obj):
        return jsonify(obj)

    @route('/', 'GET')
    def home(self):
        return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction " \
               "novels.</p> "
