import os
import json
import uuid
from postgre_backend import DatabaseConnector as dbc

def create_database_connection():
    if "DEBUG_LOCAL" in os.environ.keys():
        with open("secrets.txt", 'r') as infile:
            data = infile.read()
        credentials = json.loads(data)
        user = credentials["user"]
        password = credentials["password"]
        host = credentials["host"]
        port = credentials["port"]
        database=credentials["database"]
    else:
        user=os.environ["USER"]
        password=os.environ["PASSWORD"]
        host=os.environ["HOST"]
        port=os.environ["PORT"]
        database=os.environ["DATABASE"]

    connector = dbc(user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database)

    return connector


class LearnSupportService:

    def __init__(self):
        self.connector = create_database_connection()

    # students
    def get_student(self, student_uid):
        query = f"SELECT student_uid, name, class FROM students WHERE student_uid = '{student_uid}';"
        results = self.connector.receive_from_database(query)
        return results

    def delete_student(self, student_uid):
        query = f"DELETE FROM students WHERE student_uid = '{student_uid}';"
        self.connector.write_to_database(query)
        return True

    def get_students(self):
        query = "SELECT student_uid, name, class FROM students;"
        results = self.connector.receive_from_database(query)
        return results

    def post_students(self, name_val, class_val):
        student_uid = uuid.uuid4()
        query = f"INSERT INTO students (student_uid, name, class) VALUES ('{student_uid}', '{name_val}', '{class_val}')"
        self.connector.write_to_database(query)
        return student_uid


    # teachers
    def get_teacher(self, teacher_uid):
        query = f"SELECT teacher_uid, name FROM teachers WHERE teacher_uid = '{teacher_uid}';"
        results = self.connector.receive_from_database(query)
        return results

    def get_teacher_details(self, teacher_uid):
        query = f"SELECT contact_type, contact_reach FROM teachers_reaches WHERE teacher_uid = '{teacher_uid}' ORDER BY order_number;"
        results = self.connector.receive_from_database(query)
        return results

    def delete_teacher(self, teacher_uid):
        query = f"DELETE FROM teachers WHERE teacher_uid = '{teacher_uid}';"
        self.connector.write_to_database(query)
        return True

    def get_teachers(self):
        query = "SELECT teacher_uid, name FROM teachers;"
        results = self.connector.receive_from_database(query)
        return results

    def post_teachers(self, name_val):
        teacher_uid = uuid.uuid4()
        query = f"INSERT INTO teachers (teacher_uid, name) VALUES ('{teacher_uid}', '{name_val}')"
        self.connector.write_to_database(query)
        return teacher_uid

    def post_teacher_details(self, teacher_uid, order_number, contact_type, contact_reach):
        query = f"INSERT INTO teachers_reaches (teacher_uid, order_number, contact_type, contact_reach) VALUES ('{teacher_uid}', '{order_number}', '{contact_type}', '{contact_reach}')"
        self.connector.write_to_database(query)
        return True