import os
import uuid
from flask import Flask, request
from flask_restful import Resource, Api, abort
from postgre_backend import DatabaseConnector as dbc


def create_database_connection():
    # with open("secrets.txt", 'r') as infile:
    #     data = infile.read()
    # credentials = json.loads(data)
    # connector = dbc(user=credentials["user"],
    #                 password=credentials["password"],
    #                 host=credentials["host"],
    #                 port=credentials["port"],
    #                 database=credentials["database"])
    connector = dbc(user=os.environ["USER"],
                    password=os.environ["PASSWORD"],
                    host=os.environ["HOST"],
                    port=os.environ["PORT"],
                    database=os.environ["DATABASE"])
    return connector


app = Flask(__name__)
api = Api(app)


class Student(Resource):
    def get(self, student_uid):
        if not student_uid:
            abort(400, message="Parameter student_uid is empty.")
        else:
            query = f"SELECT student_uid, name, class FROM student WHERE student_uid = '{student_uid}';"
        results = connector.receive_from_database(query)
        if not results:
            abort(404, message="Parameter student_uid does not exist.")
        return results

    def delete(self, student_uid):
        if not student_uid:
            abort(400, message="Parameter student_uid is empty.")
        else:
            query = f"DELETE FROM student WHERE student_uid = '{student_uid}';"
        connector.write_to_database(query)
        # TODO: add better exception handling if userid does not exist in database


class Students(Resource):
    def get(self):
        query = "SELECT student_uid, name, class FROM student;"
        results = connector.receive_from_database(query)
        if not results:
            abort(404, message="No student exists.")
        return results

    def post(self):
        new_user = request.get_json()
        if not new_user:
            abort(400, message="Student is not valid.")
        student_uid = uuid.uuid4()
        query = f"INSERT INTO student (student_uid, name, class) VALUES ('{student_uid}', '{new_user['name']}', '{new_user['class']}')"
        connector.write_to_database(query)
        return {"student_uid": str(student_uid)}


# add URLs
api.add_resource(Student, '/student/<student_uid>')
api.add_resource(Students, '/student')


# TODO: make a redirect instead
@app.route('/')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    connector = create_database_connection()
    app.run(debug=False, host='0.0.0.0')
