from Controllers.Base.BaseController import BaseController


class EmployeesController(BaseController):
    @property
    def base(self):
        return self.app

    @base.route('/employees', methods=['GET'])
    def get_employees(self):
        conn = self.db.connect()  # connect to database
        query = conn.execute("select * from employees")  # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID

    @base.route('/tracks', methods=['GET'])
    def get_tracks(self):
        conn = self.db.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return self.http_response(result)

    @base.route('/employees/<employee_id>', methods=['GET'])
    def get_employees_name(self, employee_id):
        conn = self.db.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return self.http_response(result)
