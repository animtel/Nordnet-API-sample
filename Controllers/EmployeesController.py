from flask import Blueprint
from sqlalchemy import create_engine
from Controllers.Base.BaseController import http_response

employees_cotroller = Blueprint('employees_cotroller', __name__)
__db_connect = create_engine('sqlite:///chinook.db')


@employees_cotroller.route('/', methods=['GET'])
def get_employees_cotroller():
    conn = __db_connect.connect()  # connect to database
    query = conn.execute("select * from employees")  # This line performs query and returns json result
    return {'employees_cotroller': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID


@employees_cotroller.route('/tracks', methods=['GET'])
def get_tracks():
    conn = __db_connect.connect()
    query = conn.execute("select trackid, name, composer, unitprice from tracks;")
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    return http_response(result)


@employees_cotroller.route('/<employee_id>', methods=['GET'])
def get_employees_cotroller_name(employee_id):
    conn = __db_connect.connect()
    query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    return http_response(result)
