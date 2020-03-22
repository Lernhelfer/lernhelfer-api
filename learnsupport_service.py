import os
import json
import uuid
from collections import defaultdict
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
        print("no debug mode")
        user = os.environ["USER"]
        password = os.environ["PASSWORD"]
        host = os.environ["HOST"]
        port = os.environ["PORT"]
        database = os.environ["DATABASE"]

    print(user)
    print(host)
    connector = dbc(user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database)

    return connector


class LearnSupportService:

    def __init__(self):
        self.connector = create_database_connection()

    # basics
    def get_grades(self):
        query = f"SELECT grade FROM grades;"
        results = self.connector.receive_all_from_database(query)
        return results

    def get_subjects(self):
        query = f"SELECT subject_name FROM subjects;"
        results = self.connector.receive_all_from_database(query)
        return results

    def get_topics(self, subject_name, grade):
        query = f"SELECT topic_name FROM topics WHERE subject_name='{subject_name}' AND grade='{grade}';"
        results = self.connector.receive_all_from_database(query)
        return results


    # students
    def get_students(self):
        query = "SELECT student_uid, name, grade FROM students;"
        results = self.connector.receive_all_from_database(query)
        return results

    def get_student(self, student_uid):
        query = f"SELECT student_uid, name, grade FROM students WHERE student_uid = '{student_uid}';"
        results = self.connector.receive_one_from_database(query)
        return results

    def post_students(self, name_val, grade_val):
        student_uid = uuid.uuid4()
        query = f"INSERT INTO students (student_uid, name, grade) VALUES ('{student_uid}', '{name_val}', '{grade_val}')"
        self.connector.write_to_database(query)
        return student_uid

    def delete_student(self, student_uid):
        query = f"DELETE FROM students WHERE student_uid = '{student_uid}';"
        self.connector.write_to_database(query)
        return True


    # teachers
    def get_teachers(self):
        query = "SELECT teacher_uid, name, help_count FROM teachers;"
        results = self.connector.receive_all_from_database(query)
        return results

    def get_teacher(self, teacher_uid):
        query = f"SELECT teacher_uid, name, help_count FROM teachers WHERE teacher_uid = '{teacher_uid}';"
        results = self.connector.receive_one_from_database(query)
        return results

    def post_teachers(self, name_val):
        teacher_uid = uuid.uuid4()
        query = f"INSERT INTO teachers (teacher_uid, name) VALUES ('{teacher_uid}', '{name_val}')"
        self.connector.write_to_database(query)
        return teacher_uid

    def delete_teacher(self, teacher_uid):
        query = f"DELETE FROM teachers WHERE teacher_uid = '{teacher_uid}';"
        self.connector.write_to_database(query)
        return True


    # teacher profile
    def get_teacher_profile(self, teacher_uid):
        teacher_profile = {}
        teacher_details = {}
        # get profileImage
        query = f"SELECT name, helpCount, profileImageUrl FROM teachers WHERE teacher_uid = '{teacher_uid}';"
        results = self.connector.receive_one_from_database(query)
        teacher_profile["name"] = results[0]
        teacher_profile["helpCount"] = results[1]
        teacher_details["profileImageUrl"] = results[2]
        # build subjects
        query = f"SELECT subject_name, topic_name FROM teachers_topics WHERE teacher_uid = '{teacher_uid}';"
        results = self.connector.receive_all_from_database(query)
        res_dict = defaultdict(list)
        for tup in results:
            res_dict[tup[0]].append(tup[1])
        teacher_details["subjects"] = res_dict
        # build communicationMethods
        query = f"SELECT contact_type, contact_reach FROM teachers_reaches WHERE teacher_uid = '{teacher_uid}' ORDER BY order_number;"
        results = self.connector.receive_all_from_database(query)
        res_dict = defaultdict(list)
        for tup in results:
            res_dict[tup[0]].append(tup[1])
        teacher_details["communicationMethods"] = res_dict
        teacher_profile["teacherDetails"] = teacher_details
        return teacher_profile

    def post_teacher_profile(self, teacher_profile):
        #TODO: check if teacher_profile is JSON or string?
        teacher_uid = teacher_profile['teacher_uid']
        name_val = teacher_profile['name']
        teacher_details = teacher_profile['teacherDetails']
        profile_image = teacher_details['profileImageUrl']
        subjects = []
        for k, vals in teacher_details['subjects'].items():
            for v in vals:
                subjects.append((k, v))
        communication_methods = []
        for k, vals in teacher_details['communicationMethods'].items():
            for v in vals:
                communication_methods.append((k, v))

        query = f"UPDATE teachers SET name='{name_val}', profileImageUrl='{profile_image}' WHERE teacher_uid = '{teacher_uid}';"
        self.connector.write_to_database(query)

        query = f"DELETE teachers_subjects_topics WHERE teacher_uid = '{teacher_uid}';"
        self.connector.write_to_database(query)

        for sub in subjects:
            subject_id = self.get_subject_id(sub[0])
            topic_id = self.get_topic_id(sub[1])
            query = f"INSERT INTO teachers_subjects_topics (teacher_uid, subject_id, topic_id) VALUES ('{teacher_uid}', {subject_id}', '{topic_id}');"
            self.connector.write_to_database(query)

        query = f"DELETE teachers_reaches WHERE teacher_uid = '{teacher_uid}';"
        self.connector.write_to_database(query)

        for idx, meth in enumerate(communication_methods):
            query = f"INSERT INTO teachers_reaches (teacher_uid, order_number, contact_type, contact reach) VALUES ('{teacher_uid}', {idx}', '{meth[0]}', '{meth[1]}');"
            self.connector.write_to_database(query)
        return True

    def put_teacher_profile(self, teacher_profile):
        #TODO: check if teacher_profile is JSON or string?
        teacher_uid = teacher_profile['teacher_uid']
        name_val = teacher_profile['name']
        teacher_details = teacher_profile['teacherDetails']
        profile_image = teacher_details['profileImageUrl']
        subjects = []
        for k, vals in teacher_details['subjects'].items():
            for v in vals:
                subjects.append((k, v))
        communication_methods = []
        for k, vals in teacher_details['communicationMethods'].items():
            for v in vals:
                communication_methods.append((k, v))

        query = f"UPDATE teachers SET name='{name_val}', profileImageUrl='{profile_image}' WHERE teacher_uid = '{teacher_uid}';"
        self.connector.write_to_database(query)

        query = f"DELETE teachers_subjects_topics WHERE teacher_uid = '{teacher_uid}';"
        self.connector.write_to_database(query)

        for sub in subjects:
            subject_id = self.get_subject_id(sub[0])
            topic_id = self.get_topic_id(sub[1])
            query = f"INSERT INTO teachers_subjects_topics (teacher_uid, subject_id, topic_id) VALUES ('{teacher_uid}', {subject_id}', '{topic_id}');"
            self.connector.write_to_database(query)

        query = f"DELETE teachers_reaches WHERE teacher_uid = '{teacher_uid}';"
        self.connector.write_to_database(query)

        for idx, meth in enumerate(communication_methods):
            query = f"INSERT INTO teachers_reaches (teacher_uid, order_number, contact_type, contact reach) VALUES ('{teacher_uid}', {idx}', '{meth[0]}', '{meth[1]}');"
            self.connector.write_to_database(query)
        return True


    # learnRequest
    def get_learn_response(self):
        all_learn_requests_list = []
        query = f"SELECT learnRequestId, lastModificationDate, studentUid, subject, image, question, status FROM learn_requests;"
        results = self.connector.receive_all_from_database(query)

        for res in results:
            learn_response_dict = {}
            query = f"SELECT topic_id FROM learn_requests_topics WHERE learnRequestId = '{res[0]}';"
            topic_ids = self.connector.receive_all_from_database(query)
            topic_names = []
            for tid in topic_ids:
                topic_names.append(self.get_topic_name())
            learn_response_dict['topics'] = topic_names
            learn_response_dict['learnRequestId'] = res[0]
            learn_response_dict['lastModificationDate'] = res[1]
            learn_response_dict['studentUid'] = res[2]
            learn_response_dict['subject'] = res[3]
            learn_response_dict['image'] = res[4]
            learn_response_dict['question'] = res[5]
            learn_response_dict['status'] = res[6]

            all_learn_requests_list.append(learn_response_dict)

        return all_learn_requests_list
