import json
import uuid
from postgre_backend import DatabaseConnector as dbc

def create_database_connection():
    with open("secrets.txt", 'r') as infile:
        data = infile.read()
    credentials = json.loads(data)
    connector = dbc(user=credentials["user"],
                    password=credentials["password"],
                    host=credentials["host"],
                    port=credentials["port"],
                    database=credentials["database"])
    # connector = dbc(user=os.environ["USER"],
    #                 password=os.environ["PASSWORD"],
    #                 host=os.environ["HOST"],
    #                 port=os.environ["PORT"],
    #                 database=os.environ["DATABASE"])
    return connector

class LearnSupportService:
    def __init__(self):
        self.connector = create_database_connection()

    def get_student(self, student_uid):
        query = f"SELECT student_uid, name, class FROM student WHERE student_uid = '{student_uid}';"
        results = self.connector.receive_from_database(query)
        return results

    def delete_student(self, student_uid):
        query = f"DELETE FROM student WHERE student_uid = '{student_uid}';"
        self.connector.write_to_database(query)
        return True

    def get_students(self):
        query = "SELECT student_uid, name, class FROM student;"
        results = self.connector.receive_from_database(query)
        return results

    def post_students(self, name_val, class_val):
        student_uid = uuid.uuid4()
        query = f"INSERT INTO student (student_uid, name, class) VALUES ('{student_uid}', '{name_val}', '{class_val}')"
        self.connector.write_to_database(query)
        return student_uid